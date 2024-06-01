from unittest import mock

import pytest

from snowflake.core._internal.utils import ApiClientType
from snowflake.core.compute_pool._generated.api.compute_pool_api import ComputePoolApi
from snowflake.core.compute_pool._generated.api_client import ApiClient as ComputePoolApiClient
from snowflake.core.database._generated.api.database_api import DatabaseApi
from snowflake.core.database._generated.api_client import ApiClient as DatabaseApiClient
from snowflake.core.image_repository._generated.api.image_repository_api import ImageRepositoryApi
from snowflake.core.image_repository._generated.api_client import ApiClient as ImageRepositoryApiClient
from snowflake.core.schema._generated.api.schema_api import SchemaApi
from snowflake.core.schema._generated.api_client import ApiClient as SchemaApiClient
from snowflake.core.service._generated.api.service_api import ServiceApi
from snowflake.core.service._generated.api_client import ApiClient as ServiceApiClient
from snowflake.core.table._generated.api.table_api import TableApi
from snowflake.core.table._generated.api_client import ApiClient as TableApiClient
from snowflake.core.task._generated.api.task_api import TaskApi
from snowflake.core.task._generated.api_client import ApiClient as TaskApiClient
from snowflake.core.warehouse._generated.api.warehouse_api import WarehouseApi
from snowflake.core.warehouse._generated.api_client import ApiClient as WarehouseApiClient


pytestmark = pytest.mark.jenkins


def logging_message_on_change_api_client(api_client_type):
    return f"Going to use client-{api_client_type.name} for this resource"

@pytest.mark.parametrize("resource_api, resource_api_client", [
    (ComputePoolApi, ComputePoolApiClient),
    (DatabaseApi, DatabaseApiClient),
    (ImageRepositoryApi, ImageRepositoryApiClient),
    (SchemaApi, SchemaApiClient),
    (ServiceApi, ServiceApiClient),
    (TaskApi, TaskApiClient),
    (TableApi, TableApiClient),
    (WarehouseApi, WarehouseApiClient),])
@pytest.mark.usefixtures("logger_level_info")
def test_api_client_source_change(fake_root, resource_api, resource_api_client, caplog):
    # Test each Api's general client choosing mechanism
    fake_resource = mock.MagicMock()

    api = resource_api(fake_root, fake_resource, None, None)
    assert api._chosen_client_type == ApiClientType.NONE
    caplog.clear()

    # Test changing Api Client None -> Bridge
    fake_root._can_use_rest_api = False
    fake_resource._supports_rest_api = False
    assert api.api_client is None
    assert logging_message_on_change_api_client(ApiClientType.BRIDGE) in caplog.text
    caplog.clear()
    assert api._chosen_client_type == ApiClientType.BRIDGE

    # Test changing Api Client Bridge -> Rest
    fake_root._can_use_rest_api = True
    fake_resource._supports_rest_api = True
    assert isinstance(api.api_client, resource_api_client)
    assert logging_message_on_change_api_client(ApiClientType.REST) in caplog.text
    caplog.clear()
    assert api._chosen_client_type == ApiClientType.REST

    # Test changing Api Client Rest -> Bridge
    fake_root._can_use_rest_api = True
    fake_resource._supports_rest_api = False
    assert api.api_client is None
    assert logging_message_on_change_api_client(ApiClientType.BRIDGE) in caplog.text
    caplog.clear()
    assert api._chosen_client_type == ApiClientType.BRIDGE

    # Test no change api client
    fake_root._can_use_rest_api = False
    fake_resource._supports_rest_api = True
    assert api.api_client is None
    assert logging_message_on_change_api_client(ApiClientType.BRIDGE) not in caplog.text
    assert logging_message_on_change_api_client(ApiClientType.REST) not in caplog.text
    caplog.clear()
    assert api._chosen_client_type == ApiClientType.BRIDGE

    # Test changing Api Client None -> Rest
    api = resource_api(fake_root, fake_resource, None, None)
    assert api._chosen_client_type == ApiClientType.NONE
    fake_root._can_use_rest_api = True
    fake_resource._supports_rest_api = True
    assert isinstance(api.api_client, resource_api_client)
    assert logging_message_on_change_api_client(ApiClientType.REST) in caplog.text
    caplog.clear()
    assert api._chosen_client_type == ApiClientType.REST
