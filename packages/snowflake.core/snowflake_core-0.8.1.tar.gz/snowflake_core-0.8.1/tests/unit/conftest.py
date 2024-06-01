import logging

from contextlib import contextmanager
from unittest import mock

import pytest

from snowflake.core.database import DatabaseCollection
from snowflake.core.table._generated.models.table import Table
from snowflake.core.table._generated.models.table_column import TableColumn


@pytest.fixture
def fake_root():
    """Mock for Root.

    Usage of this central definition is necessary since the underlying
    generated Configuration class is handled as a singleton, so we treat
    the unit test root as a singleton as well.
    """
    mock_root = mock.MagicMock(
        _connection=mock.MagicMock(
            _rest=mock.MagicMock(
                _host="localhost",
                _protocol="http",
                _port="80",
            )
        )
    )

    mock_root._can_use_rest_api = False
    mock_root.effective_parameters(refresh = False).resource_should_use_client_bridge.return_value = False
    return mock_root

@pytest.fixture()
def logger_level_info(caplog):
    # Default logger level to info

    with caplog.at_level(logging.INFO):
        yield


@pytest.fixture
def setup_enable_rest_api_with_long_running(fake_root):
    @contextmanager
    def _setup(ref_class):
        original_can_use_rest_api = fake_root._can_use_rest_api
        fake_root._can_use_rest_api = True
        original_enable_long_running_polling = fake_root._enable_long_running_polling
        fake_root._enable_long_running_polling = True
        original_support_rest_api = ref_class._supports_rest_api
        ref_class._supports_rest_api = True

        try:
            yield
        finally:
            fake_root._can_use_rest_api = original_can_use_rest_api
            fake_root._enable_long_running_polling = original_enable_long_running_polling
            ref_class._supports_rest_api = original_support_rest_api

    return _setup


@pytest.fixture
def dbs(fake_root):
    return DatabaseCollection(fake_root)


@pytest.fixture
def db(dbs):
    return dbs["my_db"]


@pytest.fixture
def schemas(db):
    return db.schemas


@pytest.fixture
def schema(schemas):
    return schemas["my_schema"]


@pytest.fixture
def tables(schema):
    return schema.tables


@pytest.fixture
def table(tables):
    return Table(
        name="my_table",
        columns=[
            TableColumn(name="c1", datatype="int"),
        ],
    )
