from dataclasses import dataclass
from typing import Literal

from sqlalchemy import Engine

from py_tests.fixtures.transaction import Transaction

@dataclass
class DBTestEnvironment:
    db_type: Literal['mssql', 'postgres']
    transaction: Transaction
    schema: str
    