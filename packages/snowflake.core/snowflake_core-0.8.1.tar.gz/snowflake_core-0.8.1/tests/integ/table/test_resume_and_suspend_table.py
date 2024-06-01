import pytest as pytest


pytestmark = pytest.mark.usefixtures("setup_rest_api_parameters_for_table")


def test_resume_and_suspend_cluster(tables, table_handle):
    table_handle.resume_recluster()
    table_handle.suspend_recluster()
