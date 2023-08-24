from typing import Dict, Generator

import pyodbc
import pytest

pytest.register_assert_rewrite('py_tests.fixtures.utils')

from py_tests.fixtures.db_test_env import DBTestEnvironment
from py_tests.fixtures.db_test_env_lifecycle import DBTestEnvironmentLifecycle
from py_tests.fixtures.mssql.db_test_env_lifecycle import MSSQLDBTestEnvironmentLifecycle
from py_tests.fixtures.postgres.db_test_env_lifecycle import PostgresDBTestEnvironmentLifecycle
from py_tests.fixtures.sqlite3.db_test_env_lifecycle import SQLite3DBTestEnvironmentLifecycle
from py_tests.fixtures.transaction import NoCommitTransaction
from py_tests.fixtures.utils import get_env_or_default_with_warn
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

test_db_name = get_env_or_default_with_warn("TEST_DB_NAME", "____sqlalchemy_loadump_test____")

db_url_map_for_middleware_lifecycle = {
    "mssql": URL.create(
        "mssql+pyodbc",
        username=get_env_or_default_with_warn("MSSQL_USER", "sa"),
        password=get_env_or_default_with_warn("MSSQL_PASSWORD", "sqlalchemy_loadump_password0"),
        host=get_env_or_default_with_warn("MSSQL_HOST", "localhost"),
        port=int(get_env_or_default_with_warn("MSSQL_PORT", "1433")),
        database="master",
        query={"driver": pyodbc.drivers()[0], "Encrypt": "no"},
    ),
    "postgres": URL.create(
        "postgresql+psycopg2",
        username=get_env_or_default_with_warn("POSTGRES_USER", "postgres"),
        password=get_env_or_default_with_warn("POSTGRES_PASSWORD", "sqlalchemy_loadump_password0"),
        host=get_env_or_default_with_warn("POSTGRES_HOST", "localhost"),
        port=int(get_env_or_default_with_warn("POSTGRES_PORT", "5432")),
    ),
    "sqlite3": URL.create(
        "sqlite",
        database="sqlalchemy_loadump_test.sqlite3"
    ),
}

db_url_map = {
    "mssql": URL.create(
        "mssql+pyodbc",
        username=get_env_or_default_with_warn("MSSQL_USER", "sa"),
        password=get_env_or_default_with_warn("MSSQL_PASSWORD", "sqlalchemy_loadump_password0"),
        host=get_env_or_default_with_warn("MSSQL_HOST", "localhost"),
        port=int(get_env_or_default_with_warn("MSSQL_PORT", "1433")),
        database=test_db_name,
        query={"driver": pyodbc.drivers()[0], "Encrypt": "no"},
    ),
    "postgres": URL.create(
        "postgresql+psycopg2",
        username=get_env_or_default_with_warn("POSTGRES_USER", "postgres"),
        password=get_env_or_default_with_warn("POSTGRES_PASSWORD", "sqlalchemy_loadump_password0"),
        host=get_env_or_default_with_warn("POSTGRES_HOST", "localhost"),
        port=int(get_env_or_default_with_warn("POSTGRES_PORT", "5432")),
        database=test_db_name,
    ),
    "sqlite3": URL.create(
        "sqlite",
        database="sqlalchemy_loadump_test.sqlite3"
    ),
}

db_test_env_lifecycle_map: Dict[str, DBTestEnvironmentLifecycle] = {
    "mssql": MSSQLDBTestEnvironmentLifecycle(),
    "postgres": PostgresDBTestEnvironmentLifecycle(),
    "sqlite3": SQLite3DBTestEnvironmentLifecycle(),
}

db_schema_map = {
    "mssql": "dbo",
    "postgres": None,
    "sqlite3": None,
}


@pytest.fixture(params=["mssql", "postgres", "sqlite3"], scope="session")
def db_test_env(request) -> Generator[DBTestEnvironment, None, None]:
    db_type = request.param
    db_test_env_lifecycle = db_test_env_lifecycle_map[db_type]
    db_schema = db_schema_map[db_type]

    # Setup middleware
    engine_for_middleware_lifecycle = create_engine(
        db_url_map_for_middleware_lifecycle[db_type], echo=False
    )
    db_test_env_lifecycle.setup_middleware(engine_for_middleware_lifecycle, test_db_name)

    # Setup db and yield test env
    engine = create_engine(db_url_map[db_type], echo=False)
    with engine.connect() as connection:
        Session = sessionmaker(bind=engine)
        with Session() as session:
            tx = NoCommitTransaction(session, engine)
            with tx:
                setup_data = db_test_env_lifecycle.setup_db(tx)

                env = DBTestEnvironment(db_type, tx, db_schema, setup_data)
                yield env

                db_test_env_lifecycle.finalize_db(tx)

    engine.dispose()

    # Finalize middleware
    engine_for_middleware_lifecycle = create_engine(
        db_url_map_for_middleware_lifecycle[request.param], echo=False
    )
    db_test_env_lifecycle.finalize_middleware(engine_for_middleware_lifecycle, test_db_name)
