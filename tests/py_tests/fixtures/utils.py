import enum
import os
from logging import warning
from typing import Any, Dict, List, Optional, Type

import pytest


def get_env_or_default_with_warn(key: str, default: str) -> str:
    """
    Get the specified environment variable if exists, but default value with warning logging.

    :param key: The key of environment variables
    :param default: The default value if not exists.
    """
    val = os.environ.get(key)

    if val is None:
        warning(f"The specified environment variables(key={key}) is not found. Using {default}.")
        return default
    else:
        return val


def converting_table_class_type_to_schema_table_name_in_data(
    data: Dict[Type, List[Dict[str, Any]]],
    schema: Optional[str],
):
    tmp_data: Dict[str, List[Dict[str, Any]]] = {}
    for table_cls, table_data_list in data.items():
        if schema is not None:
            schema_table_name = f"{schema}.{table_cls.__tablename__}"
        else:
            schema_table_name = table_cls.__tablename__

        tmp_data[schema_table_name] = table_data_list
    return tmp_data


def assert_is_same_db_data(
    raw_data: Dict[str, List[Dict[str, Any]]], db_data: Dict[str, List[Dict[str, Any]]]
):
    assert len(raw_data) == len(db_data)
    sorted_data1_items = sorted(raw_data.items())
    sorted_data2_items = sorted(db_data.items())
    # Loop for tables
    for (tbl1, tbl_data1), (tbl2, tbl_data2) in zip(sorted_data1_items, sorted_data2_items):
        assert tbl1 == tbl2
        assert len(tbl_data1) == len(tbl_data2)
        # Loop for rows
        for row1, row2 in zip(tbl_data1, tbl_data2):
            assert len(row1) == len(row2)
            sorted_row1_items = sorted(row1.items())
            sorted_row2_items = sorted(row2.items())
            # Loop for cols
            for (col1_name, col1_val), (col2_name, col2_val) in zip(
                sorted_row1_items, sorted_row2_items
            ):
                # If the type of col_val in raw_data is Enum, db_data will be str of Enum's key.
                if isinstance(col1_val, enum.Enum):
                    col1_val = col1_val.name
                assert col1_name == col2_name
                assert col1_val == col2_val
