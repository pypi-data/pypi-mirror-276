import logging
from typing import Iterable, Optional
from abc import abstractmethod
from .result import IqlResult

logger = logging.getLogger(__name__)


class IqlDatabase:
    @abstractmethod
    def execute_query(
        self,
        query: str,
        completed_results: Iterable[IqlResult],
        parameters: Optional[Iterable] = None,
    ) -> Optional[IqlResult]:
        pass

    @abstractmethod
    def get_connection(self) -> object:
        pass

    @abstractmethod
    def close_db(self):
        pass


class IqlDatabaseConnector:
    @abstractmethod
    def create_database(self) -> IqlDatabase:
        pass

    @abstractmethod
    def create_database_from_con(self, con: object) -> IqlDatabase:
        pass
