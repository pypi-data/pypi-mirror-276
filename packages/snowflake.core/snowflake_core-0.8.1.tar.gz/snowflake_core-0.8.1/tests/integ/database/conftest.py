import pytest

from snowflake.core.database import DatabaseResource


@pytest.fixture
def ensure_rest(session, root):
    root_orig_value = root._can_use_rest_api
    root._can_use_rest_api = True
    dbr_orig_value = DatabaseResource._supports_rest_api
    DatabaseResource._supports_rest_api = True
    try:
        session.sql("alter session set enable_snow_api_for_database='enable'").collect()
        yield
    finally:
        session.sql("alter session unset enable_snow_api_for_database").collect()
        root._can_use_rest_api = root_orig_value
        DatabaseResource._supports_rest_api = dbr_orig_value
