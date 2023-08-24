from py_tests.fixtures.db_test_env import DBTestEnvironment
from py_tests.fixtures.utils import (
    assert_is_same_db_data,
    converting_table_class_type_to_schema_table_name_in_data,
)
from sqlalchemy_loadump.dumper import Dumper


def test_dumped_data_matches_setup_data(db_test_env: DBTestEnvironment):
    engine = db_test_env.transaction.engine
    session = db_test_env.transaction.session
    schema = db_test_env.schema
    setup_data = converting_table_class_type_to_schema_table_name_in_data(
        db_test_env.setup_data, schema
    )

    # Dump data from db
    dumper = Dumper(engine, session, schema)
    dumped_data = dumper.dump()

    # Check
    assert_is_same_db_data(setup_data, dumped_data)
