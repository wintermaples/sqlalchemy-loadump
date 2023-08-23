from sqlalchemy import Engine
from py_tests.fixtures.db_test_env import DBTestEnvironment
import abc

from py_tests.fixtures.transaction import Transaction


class DBTestEnvironmentLifecycle(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        pass

    def setup_middleware(self, engine: Engine, db_name: str):
        """
        Setup Database middleware.

        This function has responsibility to close the engine.
        """
        pass

    def setup_db(self, tx: Transaction):
        """
        Setup Database middleware.

        This function doesn't have responsibility to close the engine.
        """
        pass

    def finalize_db(self, tx: Transaction):
        """
        Finalize Database middleware.

        This function has responsibility to close the engine.
        """
        pass

    def finalize_middleware(self, engine: Engine, db_name: str):
        """
        Finalize Database middleware.

        This function doesn't have responsibility to close the engine.
        """
        pass
