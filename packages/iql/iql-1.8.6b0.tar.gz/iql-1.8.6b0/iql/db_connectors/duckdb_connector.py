import duckdb
import logging
from contextlib import nullcontext
from typing import Optional, Iterable

# from pandas import DataFrame
from pandas import ArrowDtype
from pyarrow import Table

from ..datamodel.database import IqlDatabaseConnector, IqlDatabase, IqlResult
import threading

from dataclasses import dataclass

logger = logging.getLogger(__name__)


def rename_dupe_arrow_columns(pat: Table) -> Table:
    # PyArrow can't export to Pandas if there are duplicate columns
    cols = pat.column_names
    unique_cols = set(cols)

    if len(unique_cols) == len(cols):
        # everything is unique
        return pat
    else:
        logger.warning("Has dupes, %s", cols)

        newcols = []
        for col in cols:
            idx = 1
            newcol = col

            while newcol in newcols:
                newcol = f"{col}_{idx}"
                idx += 1

            newcols.append(newcol)

        pat = pat.rename_columns(newcols)

        return pat


@dataclass
class DuckDbResult(IqlResult):
    _table: Table

    def arrow(self):
        return self._table

    def df_numpy(self):
        return self._table.to_pandas()

    def df_arrow(self):
        return self._table.to_pandas(types_mapper=ArrowDtype)

    def native(self):
        return self._table


@dataclass
class _DuckDB(IqlDatabase):
    _connection: object
    _started_thread: int

    def execute_query(
        self,
        query: str,
        completed_results: Optional[Iterable[IqlResult]] = None,
        parameters: Optional[Iterable] = None,
    ) -> Optional[DuckDbResult]:
        """param: Each of the completed _dfs are registered to the database.
        threaded: pass True to run in a separate connection, otherwise runs in main connection
        """
        if len(query.strip()) == 0:
            return None

        threaded = threading.get_ident() != self._started_thread

        # create & close the connection if we're threading, otherwise create one
        with (
            self.get_connection() if threaded else nullcontext(self._connection)
        ) as con:
            try:
                # Register each of the dataframes to duckdb, so duckdb can query them
                # Other database might require a "load" or "from_pandas()" step to load these
                # to temporary tables.
                if completed_results is not None:
                    for result in completed_results:
                        data = result.native()
                        con.register(result.name, data)  # type: ignore

                d = con.sql(query, params=parameters)  # type: ignore
                if d is not None:
                    table = d.arrow()
                    table = rename_dupe_arrow_columns(table)
                    return DuckDbResult(name=query, query=query, _table=table)

                else:
                    return None
            except Exception as e:
                logger.exception("Error executing SQL DFs: %s", query)
                raise ValueError(f"Error executing {query}") from e

    def get_connection(self):
        return self._connection.cursor()  # type: ignore

    def close_db(self):
        self._connection.close()  # type: ignore
        self._connection = None


class _DuckDbConnector(IqlDatabaseConnector):
    def create_database(self, file=":memory:") -> _DuckDB:
        con = duckdb.connect(database=file)
        # con.execute("SET enable_progress_bar=false;")
        return _DuckDB(_connection=con, _started_thread=threading.get_ident())

    def create_database_from_con(self, con: object) -> _DuckDB:
        return _DuckDB(_connection=con, _started_thread=threading.get_ident())


def getConnector() -> IqlDatabaseConnector:
    return _DuckDbConnector()
