import importlib
import logging
from functools import lru_cache
from pathlib import Path
from typing import Dict, Iterable, Optional, Tuple, Union

import sqlparse
from pandas import DataFrame

from . import constants, options_parser
from .datamodel.database import IqlDatabaseConnector
from .datamodel.extension import IqlExtension
from .datamodel.querycontainer import IqlQueryContainer
from .datamodel.result import IqlResult
from .utils import extract_subquery_strings

logger = logging.getLogger(__name__)

# Customizations #
# Configure before first use
# Note: Will likely move these to a config file
DB_MODULE: str = "iql.db_connectors.duckdb_connector"  # Change before first db use
DFPREFIX: str = "iqldf"  # Prefix for temporary files
DEFAULT_EXT_DIRECTORY = None  # Sets temp dir for extensions, set before extension use

# Internal Objects
_EXTENSIONS: Dict[Tuple[str, str], IqlExtension] = {}  # register_extension
_DBCONNECTOR: Optional[IqlDatabaseConnector] = None  # Set DB_MODULE before use.
_SUBSTITUTIONS: Dict[str, str] = {}  # Substition map: any occurence in a query of key will be replaced by value
_ALIASES: Dict[str, Union[str, Path]] = {}  # register_alias


def _parameterize_sql_alias(subword, query) -> str:
    if subword not in _ALIASES.keys():
        raise ValueError(f"Unknown alias {subword}")

    query_data = _ALIASES[subword]
    base_query = query_data if isinstance(query_data, str) else query_data.read_text()

    for k, v in options_parser.options_to_list(query).items():
        # convert the parameter to $uppercase, so security => $SECURITY
        newk = f"${k.upper()}"
        base_query = base_query.replace(newk, str(v))

    return base_query


def replace_sql_aliases(query) -> str:
    newquery = query
    for keyword, subword, outer, inner in extract_subquery_strings(query, ["alias"]):
        sql = _parameterize_sql_alias(subword, outer)

        # aliases might recurse
        sql = replace_sql_aliases(sql)
        logger.debug("Found SQL alias, replacing and parameterizing: %s", outer)

        newquery = newquery.replace(outer, sql)

    return newquery


@lru_cache(maxsize=3)
def parse_sql(query: str):
    return sqlparse.parse(query)


def execute_debug(
    query: str,
    con: Optional[object] = None,
    substitutions: Optional[Dict[str, str]] = None,
    parameters: Optional[Iterable] = None,
) -> Tuple[bool, Optional[DataFrame], Optional[Dict[str, Iterable[IqlResult]]]]:
    """Returns the success (True or False), final query result, and the debug
    results: all the intermediate queries and subqueries."""
    # Connection to database

    # Special case for BQL only.
    if query.strip().startswith("get") or query.strip().startswith("let"):
        query = query.replace('"', '\\"')
        query = f'''select * from bql("""{query}""")'''

    # Initialize or Reuse DB Connector
    idc: IqlDatabaseConnector = get_dbconnector()

    if con is None:
        db = idc.create_database()
    else:
        db = idc.create_database_from_con(con=con)

    origquery = None

    while query != origquery:
        # Keep changing until all changes and aliases are updated
        # Since an alias can have a substitution, and a substitution can have an alias
        # We just need to repeat

        origquery = query

        if substitutions is None:
            newsubs = _SUBSTITUTIONS
        else:  # override any substitutions
            newsubs = _SUBSTITUTIONS.copy()
            newsubs.update(substitutions)

        logger.debug("Substituting with %s, query=%s", newsubs, query)
        for k, v in newsubs.items():
            # logger.debug("%s %s", k, v)
            # TODO: Remove the $, and use exact SUBSTITUTIONS. Makes it easier to use whatever
            # substitution syntax you want.
            # TODO: Consider how to support both JINJA and native
            query = query.replace(f"${k.upper()}", str(v))
        # Aliases
        query = replace_sql_aliases(query)

    logger.debug("Updated query %s", query)

    try:
        # A single query might contain multiple SQL statements. Parse them out and iterate:
        df = None
        completed_result_map = {}
        if ";" not in query:
            # Performance optimization for simple queries
            iqc = IqlQueryContainer(query=query, db=db, substitutions=substitutions)  # type: ignore

            df, completed_results = iqc.execute(parameters=parameters)
            return (True, df, {query: completed_results})
        else:
            logger.debug("Parsing %.120s", query)

            statements = parse_sql(query)

            for i, statement in enumerate(statements):
                singlequery = statement.value.strip(";")
                iqc = IqlQueryContainer(
                    query=singlequery,
                    db=db,
                    substitutions=substitutions,  # type: ignore
                )

                # Run each statement, but only keep the results from the last one

                if (
                    i == len(statements) - 1
                ):  # Only pass parameters to last query. This is consistent with how duckdb would run this natively.
                    df, completed_results = iqc.execute(parameters=parameters)
                else:
                    df, completed_results = iqc.execute()
                completed_result_map[statement] = completed_results

        return (True, df, completed_result_map)

    finally:
        if con is None:  # DB was created here, so close it
            db.close_db()


def execute(
    query: str,
    con: Optional[object] = None,
    substitutions: Optional[Dict[str, str]] = None,
    parameters: Optional[Iterable] = None,
) -> Optional[DataFrame]:
    """Executes the given SQL query. Keyword is only used to run a single subquery without SQL."""

    success, df, completed_results = execute_debug(query, con, substitutions=substitutions, parameters=parameters)

    return df


def executedf(*args, **kwargs) -> DataFrame:
    """Helper that enforces that a DataFrame is returned, otherwise ValueError"""

    df = execute(*args, **kwargs)

    if df is None:
        raise ValueError("Execution returned a None result")
    else:
        return df


def get_dbconnector() -> IqlDatabaseConnector:
    global _DBCONNECTOR
    if _DBCONNECTOR is None:
        # Initializes only on first reference
        module = importlib.import_module(DB_MODULE)
        _DBCONNECTOR = module.getConnector()

    assert _DBCONNECTOR is not None  # getConnector should raise

    return _DBCONNECTOR


def register_extension(e: IqlExtension):
    _EXTENSIONS[(e.keyword, e.subword)] = e  # type: ignore
    if e.keyword not in constants._KNOWN_EXTENSIONS.keys():
        constants._KNOWN_EXTENSIONS[e.keyword] = e.keyword

    if e.temp_file_directory is None:
        e.temp_file_directory = DEFAULT_EXT_DIRECTORY


def register_alias(subword: str, data: Union[str, Path]):
    """
    Aliases are called via
    alias.aliasname(param1=abc, param2.abc)
    When run, the alias will be replaced, and "$PARAM1" will be replaced with abc.
    You can either register the entire SQL or a path to a file containing the SQL.

    If a Path is given, then it is loaded on each access (not cached).
    """

    logger.debug("Registering alias: %s", subword)
    _ALIASES[subword] = data


def list_extensions() -> Iterable[str]:
    return list(constants._KNOWN_EXTENSIONS.keys())


def get_extension(keyword: str, subword: str) -> IqlExtension:
    """Loads extension on first use"""

    words = (keyword, subword)
    if words in _EXTENSIONS:
        return _EXTENSIONS[words]
    elif keyword not in constants._KNOWN_EXTENSIONS.keys():
        raise ValueError(f"Unknown Extension {keyword}")
    else:
        # Dynamically load extensions on first use
        # This avoids requiring installation of packages that
        # aren't needed
        classname = constants._KNOWN_EXTENSIONS[keyword]
        module = importlib.import_module(classname)
        module.register(keyword)

        if words not in _EXTENSIONS:
            raise ValueError(f"{keyword}.{subword} is not registered")
        return _EXTENSIONS[words]


def configure(temp_dir: Optional[str] = None):
    """
    Must be called before extensions are initialized (on first use)
    duration_seconds: None (Disabled), -1 (Infinite), int (Seconds)
    file_directory: None (no file cache), string (output directory)
    """
    global DEFAULT_EXT_DIRECTORY
    DEFAULT_EXT_DIRECTORY = temp_dir
