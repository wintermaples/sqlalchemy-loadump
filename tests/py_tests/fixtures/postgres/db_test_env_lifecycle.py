import datetime
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import Engine, text
from py_tests.fixtures.db_models_for_test import Base, EnumClass, TypeTest
from py_tests.fixtures.db_test_env_lifecycle import DBTestEnvironmentLifecycle
from py_tests.fixtures.db_test_env import DBTestEnvironment
from py_tests.fixtures.transaction import Transaction


class PostgresDBTestEnvironmentLifecycle(DBTestEnvironmentLifecycle):
    def setup_middleware(self, engine: Engine, db_name: str):
        autocommit_engine = engine.execution_options(isolation_level="AUTOCOMMIT")
        with autocommit_engine.connect() as connection:
            connection.execute(text(f"CREATE DATABASE {db_name}"))
        autocommit_engine.dispose()
        engine.dispose()

    def setup_db(self, tx: Transaction):
        # Create table
        Base.metadata.create_all(bind=tx.engine)

        # Insert test data
        type_test = TypeTest(
            id_=1,
            big_integer=2**31 - 1,
            boolean=False,
            date=datetime.date.today(),
            date_time=datetime.datetime.now(),
            double_=0.1,
            enum=EnumClass.A,
            float_=0.1,
            integer=2**15 - 1,
            interval=datetime.timedelta(days=10),
            large_binary="testbytes".encode("utf-8"),
            numeric=Decimal("-1.2345"),
            small_integer=2**8 - 1,
            string="string",
            text="text",
            time=datetime.time(hour=1, minute=2, second=3, microsecond=123),
            unicode="unicode",
            unicode_text="unicode_text",
            uuid=uuid4(),
        )
        tx.session.add(type_test)
        tx.session.flush()

    def finalize_middleware(self, engine: Engine, db_name: str):
        autocommit_engine = engine.execution_options(isolation_level="AUTOCOMMIT")
        with autocommit_engine.connect() as connection:
            connection.execute(text(f"DROP DATABASE {db_name}"))
        autocommit_engine.dispose()
        engine.dispose()
