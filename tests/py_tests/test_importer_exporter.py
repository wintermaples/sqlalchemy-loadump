from pathlib import Path
import pytest
from sqlalchemy import MetaData, delete
from py_tests.fixtures.db_test_env import DBTestEnvironment
from py_tests.fixtures.utils import assert_is_same_db_data, converting_table_class_type_to_schema_table_name_in_data
from sqlalchemy_loadump.dumper import Dumper
from sqlalchemy_loadump.exporter.json_exporter import JSONExporter
from sqlalchemy_loadump.importer.json_importer import JSONImporter
from sqlalchemy_loadump.loader import Loader


@pytest.mark.parametrize(
        argnames=["human_readable"],
        argvalues=[
            (True,),
            (False,),
        ]
)
def test_json_exporter_dump_export_import_load_dump_is_same(db_test_env: DBTestEnvironment, human_readable: bool):
    engine = db_test_env.transaction.engine
    session = db_test_env.transaction.session
    schema = db_test_env.schema
    setup_data = converting_table_class_type_to_schema_table_name_in_data(
        db_test_env.setup_data, schema
    )

    file_path = Path("./dump.json")

    with session.begin_nested() as nested:
        ##### Dump #####
        # Dump data from db
        dumper = Dumper(engine, session, schema)
        dumped_data = dumper.dump()
        # Check
        assert_is_same_db_data(setup_data, dumped_data)
        ################

        ##### Export #####
        json_exporter = JSONExporter()
        json_exporter.export_to_file(dumped_data, file_path, human_readable)
        ################

        ##### Import #####
        json_importer = JSONImporter()
        imported_data = json_importer.import_from_file(file_path)
        ################

        ##### Load #####
        # Delete old data
        metadata = MetaData(schema=schema)
        metadata.reflect(bind=engine)
        for table in reversed(metadata.sorted_tables):
            session.execute(delete(table))
        session.flush()

        # Load data from imported data to db
        loader = Loader(imported_data, engine, session, schema)
        loader.load()
        ################

        ##### Dump #####
        # Dump data from db
        dumper = Dumper(engine, session, schema)
        dumped_data = dumper.dump()
        # Check
        assert_is_same_db_data(setup_data, dumped_data)
        ################

        nested.rollback()
