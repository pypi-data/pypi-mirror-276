#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

import pytest

from snowflake.core._internal.utils import ApiClientType


pytestmark = pytest.mark.jenkins


@pytest.fixture
def setup_rest_api_parameters(session, root):
    orig_value = root._can_use_rest_api
    root._can_use_rest_api = True
    try:
        yield
    finally:
        session.sql("alter session unset enable_snow_api_for_task").collect()
        root._can_use_rest_api = orig_value


# By intention, the only value for this parameter that has an effect on
# the using the bridge client is 'bridge' (case-insensitive)
@pytest.mark.parametrize("param_value,expected_client_type",
                         [("bridge", ApiClientType.BRIDGE), ("enable", ApiClientType.REST),
                          ("disable", ApiClientType.REST), ("some_other_value", ApiClientType.REST),
                          ("BrIDGe ", ApiClientType.BRIDGE)])
def test_enable_snow_api_parameter(setup_rest_api_parameters, tasks, session, param_value: str,
                                   expected_client_type: ApiClientType):
    session.sql("alter session set enable_snow_api_for_task" + "=" + param_value).collect()
    # force evaluation; assigning it a variable to avoid
    tasks._api._root._refresh_parameters()
    tasks._api.api_client #noqa: B018
    assert tasks._api._chosen_client_type == expected_client_type
