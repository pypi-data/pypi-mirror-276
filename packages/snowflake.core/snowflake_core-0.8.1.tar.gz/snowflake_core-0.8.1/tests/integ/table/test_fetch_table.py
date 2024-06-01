import pytest as pytest

from tests.integ.table.conftest import assert_table


pytestmark = pytest.mark.usefixtures("setup_rest_api_parameters_for_table")


@pytest.mark.skip_rest
def test_fetch(tables, table_handle, database, schema):
    table_deep = table_handle.fetch()
    assert_table(table_deep, table_handle.name, database, schema, True)
