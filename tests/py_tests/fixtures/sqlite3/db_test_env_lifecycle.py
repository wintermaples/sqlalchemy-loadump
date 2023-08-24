import datetime
from decimal import Decimal
from typing import Any, Dict, List, Type
from uuid import uuid4

from py_tests.fixtures.db_test_env_lifecycle import DBTestEnvironmentLifecycle
from py_tests.fixtures.sqlite3.db_models import (
    Base,
    ChildTable,
    EnumOfEnumTypeTestTable,
    ParentTable,
    TypeTestTable,
)
from py_tests.fixtures.transaction import Transaction
from sqlalchemy import Engine, text


class SQLite3DBTestEnvironmentLifecycle(DBTestEnvironmentLifecycle):
    def setup_middleware(self, engine: Engine, db_name: str):
        engine.dispose()

    def setup_db(self, tx: Transaction) -> Dict[Type, List[Dict[str, Any]]]:
        # Create table
        Base.metadata.create_all(bind=tx.engine)

        # Setup data
        data = {
            TypeTestTable: [
                {
                    "id_": 1,
                    "big_integer": 2**31 - 1,
                    "boolean": False,
                    "date": datetime.date.today(),
                    "date_time": datetime.datetime.now(),
                    "double_": 0.1,
                    "enum": EnumOfEnumTypeTestTable.A,
                    "float_": 0.1,
                    "integer": 2**15 - 1,
                    "large_binary": "testbytes".encode("utf-8"),
                    "numeric": Decimal("-1"),
                    "numeric_5_3": Decimal("-12.345"),
                    "small_integer": 2**8 - 1,
                    "string": "string",
                    "text": "text",
                    "time": datetime.time(hour=1, minute=2, second=3, microsecond=123),
                    "unicode": "unicode",
                    "unicode_text": "unicode_text",
                    "uuid": uuid4(),
                }
            ],
            ParentTable: [
                {
                    "id_": 1,
                },
                {
                    "id_": 2,
                },
            ],
            ChildTable: [{"id_": 1, "parent_id": 1}],
        }

        # Insert test data
        for tbl, tds in data.items():
            for td in tds:
                row = tbl(**td)
                tx.session.add(row)
            tx.session.flush()

        return data

    def finalize_db(self, tx: Transaction):
        pass

    def finalize_middleware(self, engine: Engine, db_name: str):
        engine.dispose()
