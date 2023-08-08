from sqlite3 import IntegrityError
import warnings
from typing import Any, Dict, List, Optional

from sqlalchemy import Table, insert, select, MetaData, create_engine
from sqlalchemy.orm import Session, sessionmaker


class Loader:
    def __init__(
        self,
        dump_data: Dict[str, List[Dict[str, Any]]],
        db_url: str,
        engine_options: Dict[str, Any] = {},
        schema: Optional[str] = None,
    ):
        self.dump_data = dump_data
        self.db_url = db_url
        self.engine_options = engine_options
        self.schema = schema

    def load(self) -> None:
        engine = create_engine(self.db_url, **self.engine_options)
        session_maker = sessionmaker(bind=engine)
        metadata = MetaData(schema=self.schema)
        metadata.reflect(bind=engine)
        with session_maker() as session:
            for table_name, rows in self.dump_data.items():
                table = metadata.tables.get(table_name)
                if table is None:
                    raise IntegrityError(f"Table {table_name} not found in database.")

                for row in rows:
                    stmt = insert(table).values(**row)
                    session.execute(stmt)

            session.commit()
