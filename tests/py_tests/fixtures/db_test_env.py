from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Type


from py_tests.fixtures.transaction import Transaction


@dataclass
class DBTestEnvironment:
    db_type: str
    transaction: Transaction
    schema: str
    setup_data: Dict[Type, List[Dict[str, Any]]]
