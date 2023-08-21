import datetime
from decimal import Decimal

from typing import Generator
from uuid import uuid4
import pytest
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

from tests.db_models_for_test import Base, EnumClass, TypeTest
from tests.transaction import NoCommitTransaction, Transaction


@pytest.fixture(params=["sqlserver", "postgresql"], scope="session")
def tx_for_test(request) -> Generator[Transaction, None, None]:
    """
    Create a database transaction fixture to test.

    ## Usage
    ```
    def test_hoge(tx_for_test):
        with tx_for_test as tx:
            data = TableModel(...)
            tx.session.add(data)
            ...
    ```
    The transaction doesn't commit (but do flush) at the end of scope.

    ## Connection Information
    This is created with below connection informations.

    ### SQLServer
    - DriverName: mssql+pyodbc
    - UserName: test
    - Password: test
    - Host: localhost
    - Port: 1433
    - Database: test_sqlalchemy_loadump

    ### PostgreSQL
    - DriverName: postgresql+psycopg2
    - UserName: test
    - Password: test
    - Host: localhost
    - Port: 5432
    - Database: test_sqlalchemy_loadump
    """
    db_url_map = {
        "sqlserver": URL.create(
            "mssql+pyodbc",
            username="test",
            password="test",
            host="localhost",
            port=1433,
            database="testtest_sqlalchemy_loadump",
        ),
        "postgresql": URL.create(
            "postgresql+psycopg2",
            username="test",
            password="test",
            host="localhost",
            port=5432,
            database="test_sqlalchemy_loadump",
        ),
    }

    engine = create_engine(db_url_map[request.param], echo=False)
    Session = sessionmaker(bind=engine)

    with Session() as session:
        tx = NoCommitTransaction(session, engine)

        with tx:
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

            yield tx
