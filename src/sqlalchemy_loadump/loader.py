from sqlite3 import IntegrityError
import warnings
from typing import Any, Dict, List, Optional

from sqlalchemy import Engine, Table, delete, insert, select, MetaData, create_engine
from sqlalchemy.orm import Session, sessionmaker


class Loader:
    def __init__(
        self,
        dump_data: Dict[str, List[Dict[str, Any]]],
        engine: Engine,
        session: Session,
        schema: Optional[str],
    ):
        self.dump_data = dump_data
        self.engine = engine
        self.session = session
        self.schema = schema

    def load(self) -> None:
        metadata = MetaData(schema=self.schema)
        metadata.reflect(bind=self.engine)

        for table_name, rows in self.dump_data.items():
            table = metadata.tables.get(table_name)
            if table is None:
                raise IntegrityError(f"Table {table_name} not found in database.")

            # Bulk insert
            if len(rows) > 0:
                self.session.execute(
                    insert(table),
                    rows,
                )
