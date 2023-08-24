from typing import Any, Dict, List, Type
from sqlalchemy import Engine, Table
from py_tests.fixtures.db_test_env import DBTestEnvironment
import abc

from py_tests.fixtures.transaction import Transaction


class DBTestEnvironmentLifecycle(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def setup_middleware(self, engine: Engine, db_name: str):
        """
        Setup Database middleware.

        This function has responsibility to close the engine.
        """
        raise NotImplemented()

    @abc.abstractmethod
    def setup_db(self, tx: Transaction) -> Dict[Type, List[Dict[str, Any]]]:
        """
        Setup Database middleware.

        This function doesn't have responsibility to close the engine.

        :return: The dictionary of set up data.
        """
        raise NotImplemented()

    @abc.abstractmethod
    def finalize_db(self, tx: Transaction):
        """
        Finalize Database middleware.

        This function has responsibility to close the engine.
        """
        raise NotImplemented()

    @abc.abstractmethod
    def finalize_middleware(self, engine: Engine, db_name: str):
        """
        Finalize Database middleware.

        This function doesn't have responsibility to close the engine.
        """
        raise NotImplemented()
