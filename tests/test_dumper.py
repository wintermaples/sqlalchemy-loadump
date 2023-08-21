from typing import Generator

from tests.conftest import Transaction


def test_conftest(tx_for_test: Transaction):
    with tx_for_test as tx:
        pass

