from sqlalchemy import MetaData, delete
from py_tests.fixtures.db_test_env import DBTestEnvironment
from py_tests.fixtures.utils import (
    assert_is_same_db_data,
    converting_table_class_type_to_schema_table_name_in_data,
)
from sqlalchemy_loadump.dumper import Dumper
from sqlalchemy_loadump.loader import Loader


def test_dump_load_dump_is_same(db_test_env: DBTestEnvironment):
    engine = db_test_env.transaction.engine
    session = db_test_env.transaction.session
    schema = db_test_env.schema
    setup_data = converting_table_class_type_to_schema_table_name_in_data(
        db_test_env.setup_data, schema
    )

    with session.begin_nested() as nested:
        ##### Dump #####
        # Dump data from db
        dumper = Dumper(engine, session, schema)
        dumped_data = dumper.dump()
        # Check
        assert_is_same_db_data(setup_data, dumped_data)
        ################

        ##### Load #####
        # Delete old data
        metadata = MetaData(schema=schema)
        metadata.reflect(bind=engine)
        for table in reversed(metadata.sorted_tables):
            session.execute(delete(table))
        session.flush()

        # Load data to db
        loader = Loader(dumped_data, engine, session, schema)
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
