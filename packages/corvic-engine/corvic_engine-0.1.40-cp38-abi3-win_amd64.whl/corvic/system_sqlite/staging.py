"""Sqlite backed staging system."""

import functools
import uuid
from collections.abc import Callable, Iterable, Mapping
from typing import Final

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq
import sqlglot

from corvic.system import DataKindManager, StorageManager, VectorSimilarityMetric

_CORVIC_SIMILARTITY_TO_DUCKDB_SIMILARITY: Final[dict[VectorSimilarityMetric, str]] = {
    "cosine": "cosine",
    "euclidean": "l2sq",
}


class DuckDBStaging:
    """Access to data staged in a local database like sqlite."""

    _storage_manager: StorageManager
    _db_conn: duckdb.DuckDBPyConnection
    _vector_column_names_to_widths: dict[str, int]

    # Known tables and known row counts. As a DuckDBStaging instance is just
    # one client of possibly many clients of the underlying StorageManager
    # and duckdb instance, these counts are treated as invalidatable state
    # snapshots.
    _table_counts: dict[str, int | None]

    def __init__(
        self,
        storage_manager: StorageManager,
        db_conn: duckdb.DuckDBPyConnection,
        vector_column_names_to_sizes: dict[str, int],
    ):
        self._storage_manager = storage_manager
        self._db_conn = db_conn
        self._vector_column_names_to_widths = vector_column_names_to_sizes
        self._table_counts = {}

    def _get_tables(self) -> set[str]:
        """Returns tables known by duckdb."""
        with self._db_conn.cursor() as cur:
            cur.execute(
                """
                SELECT table_name FROM information_schema.tables
                """
            )
            result = cur.fetchall()
        return {r[0] for r in result}

    def _add_vector_indexes(self, table_name: str, raw_table_data: pa.Table):
        table_column_names = raw_table_data.column_names
        for column_name in self.vector_column_names_to_widths:
            if column_name not in table_column_names:
                continue
            for sim_metric in _CORVIC_SIMILARTITY_TO_DUCKDB_SIMILARITY.values():
                self._db_conn.execute(
                    f"""
                    CREATE INDEX '{sim_metric}_idx_{column_name}' ON {table_name}
                        USING HNSW ('{column_name}') WITH (metric = '{sim_metric}')
                    """
                )

    def _update_blobs_for_prefix(
        self,
        manager: DataKindManager,
        next_count: dict[str, int | None],
        transform_table: Callable[[str, pa.Table], None] | None = None,
    ):
        bucket = self._storage_manager.bucket
        blobs = bucket.list_blobs()
        prefix = manager.prefix
        table_blobs = [
            (
                blob,
                manager.blob_name_from_url(url=blob.url).unwrap_or_raise(),
            )
            for blob in blobs
            if blob.name.startswith(prefix)
        ]

        tables = self._get_tables()
        for blob, table_name in table_blobs:
            if table_name in tables:
                next_count[table_name] = self._table_counts.get(table_name)
                continue
            with blob.open("rb") as stream:
                table = pq.read_table(stream)
                self._db_conn.from_arrow(table).create(f'"{table_name}"')
                next_count[table_name] = table.num_rows
                if transform_table:
                    transform_table(table_name, table)

    def _update_blobs(self) -> None:
        """Adds any blobs not yet known by duckdb to duckdb as tables.

        As a side-effect, update _table_counts.
        """
        next_count: dict[str, int | None] = {}
        self._update_blobs_for_prefix(self._storage_manager.tabular, next_count)
        self._update_blobs_for_prefix(
            self._storage_manager.vector, next_count, self._add_vector_indexes
        )
        self._table_counts = next_count

    def _update_counts(self, blobs: Iterable[str]) -> None:
        """Try to update row counts for given blob tables.

        If the blob tables are not known by duckdb, no counts can be updated. Thus,
        callers should not assume that counts for the given will be known after this
        call returns.
        """
        blobs = [blob for blob in blobs if blob in self._table_counts]
        table_queries = [f"SELECT COUNT(*) FROM '{name}'" for name in blobs]
        if not table_queries:
            return

        with self._db_conn.cursor() as cur:
            cur.execute(" UNION_ALL ".join(table_queries))
            result = cur.fetchall()

        for table_name, count in zip(blobs, [r[0] for r in result], strict=True):
            self._table_counts[table_name] = int(count)

    def count_ingested_rows(self, blob_name: str, *other_blob_names: str) -> int:
        # Callers expect this function to be cheap, so reuse data where possible
        blobs = (blob_name, *other_blob_names)
        blobs_to_query = [
            blob for blob in blobs if self._table_counts.get(blob, None) is None
        ]
        if blobs_to_query:
            # This will only execute in the unlikely situation that another client
            # is adding blobs that the current client is asking for the counts of.
            self._update_blobs()
            self._update_counts(blobs_to_query)
        return sum([self._table_counts.get(blob, None) or 0 for blob in blobs])

    def query_for_blobs(
        self, blob_names: list[str], column_names: list[str]
    ) -> sqlglot.exp.Query:
        columns = [
            sqlglot.column(sqlglot.exp.to_identifier(name, quoted=True))
            for name in column_names
        ]
        tables = [
            sqlglot.to_identifier(blob_name, quoted=True) for blob_name in blob_names
        ]
        query = sqlglot.select(*columns)

        if len(tables) == 1:
            return query.from_(tables[0])

        staging_union_table = sqlglot.to_identifier(
            f"staging-{uuid.uuid4().hex}", quoted=True
        )

        union = functools.reduce(
            lambda x, y: x.union(y, distinct=False),
            (
                sqlglot.select(*column_names).from_(
                    sqlglot.table(sqlglot.to_identifier(table_name, quoted=True))
                )
                for table_name in blob_names
            ),
        )
        return (
            sqlglot.select(*column_names)
            .from_(staging_union_table)
            .with_(staging_union_table, as_=union)
        )

    def query_for_vector_search(
        self,
        input_vector: list[float],
        vector_blob_names: list[str],
        vector_column_name: str,
        column_names: list[str],
        num_results: int,
        similarity_metric: VectorSimilarityMetric,
    ) -> sqlglot.exp.Query:
        raise NotImplementedError(
            "DuckDB staging missing vector search query generation"
        )

    @property
    def vector_column_names_to_widths(self) -> Mapping[str, int]:
        return self._vector_column_names_to_widths

    def run_select_query(self, query: sqlglot.exp.Query) -> pa.RecordBatchReader:
        """Run a select query to extract and transform staging data.

        N.B. this behaves a little differently than rockset would.
        Rockset has one super-wide table, so it would silently omit data. This
        implementation will complain loudly if the query references an unstaged blob.
        That tradeoff is somewhat reasonable since if data isn't staged in this case it
        means the caller is doing something wrong (in Rockset's case there's some
        asynchrony which could lead to the data not being staged).
        """
        self._update_blobs()
        with self._db_conn.cursor() as cur:
            cur.execute(query.sql(dialect="duckdb"))
            result = cur.fetch_arrow_table()
        return result.to_reader()
