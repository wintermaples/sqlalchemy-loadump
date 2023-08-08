import warnings
from typing import Any, Dict, List, Optional

from sqlalchemy import Table, select, MetaData, create_engine, text
from sqlalchemy.orm import Session, sessionmaker


class Dumper:
    def __init__(
        self,
        db_url: str,
        engine_options: Dict[str, Any] = {},
        schema: Optional[str] = None,
    ):
        self.db_url = db_url
        self.engine_options = engine_options
        self.schema = schema

    @staticmethod
    def _dump_table(session: Session, table: Table) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        for db_columns in session.execute(select(table)):
            if len(db_columns) != len(table.columns):
                warnings.warn(
                    f"The length of columns declared != the length of columns in the real table."
                    f"({table.name}: {len(db_columns)} !=  {len(table.columns)})"
                )
                continue

            # Convert to dict
            columns = {}
            for index, column in enumerate(table.columns):
                columns[column.name] = db_columns[index]

            rows.append(columns)

        return rows

    def dump(self) -> Dict[str, List[Dict[str, Any]]]:
        engine = create_engine(self.db_url, **self.engine_options)
        session_maker = sessionmaker(bind=engine)
        metadata = MetaData(schema=self.schema)
        metadata.reflect(bind=engine)

        with session_maker() as session:
            # Table --> List of Data.
            data_list_in_tables: Dict[str, List[Dict[str, Any]]] = {}

            for table in metadata.sorted_tables:
                table_name_with_schema_name = ".".join(list(filter(lambda k: k is not None, [table.schema, table.name]))) # type: ignore
                data_list_in_tables[table_name_with_schema_name] = self._dump_table(session, table)

            return data_list_in_tables
