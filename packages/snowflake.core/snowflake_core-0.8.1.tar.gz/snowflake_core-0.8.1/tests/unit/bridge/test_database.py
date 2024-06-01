from unittest import mock

import pytest

from snowflake.core import Clone, PointOfTimeOffset
from snowflake.core._internal.bridge.rest_errors import NotFound
from snowflake.core.database import Database, DatabaseCollection
from snowflake.core.exceptions import NotFoundError, ServerError


pytestmark = pytest.mark.jenkins


def test_fetch(fake_root):
    dbs = DatabaseCollection(fake_root)
    with mock.patch(
        "snowflake.core._internal.bridge.executor.SnowExecute.execute"
    ) as mocked_execute:
        with pytest.raises(NotFoundError):
            dbs["my_db"].fetch()
    mocked_execute.assert_called_once_with(
        "SHOW DATABASES LIKE 'MY_DB' "
    )

def test_create_clone(fake_root):
    dbs = DatabaseCollection(fake_root)
    clone = Clone(
        source="other_db",
        point_of_time=PointOfTimeOffset(reference="at", when="-1800"),
    )
    with mock.patch(
        "snowflake.core._internal.bridge.executor.SnowExecute.execute"
    ) as mocked_execute:
        with pytest.raises(ServerError):
            dbs.create(
                Database(
                    name="my_db",
                ),
                kind="transient",
                clone=clone,
            )
    mocked_execute.assert_called_once_with(
        "CREATE transient DATABASE MY_DB CLONE OTHER_DB AT (OFFSET => -1800) "
    )

def test_create(fake_root):
    dbs = DatabaseCollection(fake_root)
    with mock.patch(
        "snowflake.core._internal.bridge.executor.SnowExecute.execute"
    ) as mocked_execute:
        with pytest.raises(ServerError):
            dbs.create(
                Database(
                    name="my_db",
                    max_data_extension_time_in_days=1,
                ),
                kind="transient",
            )
    mocked_execute.assert_called_once_with(
        "CREATE transient DATABASE MY_DB MAX_DATA_EXTENSION_TIME_IN_DAYS = 1 "
    )

def test_create_or_update_create(fake_root):
    dbs = DatabaseCollection(fake_root)
    with mock.patch(
        "snowflake.core._internal.bridge.executor.SnowExecute.execute"
    ) as mocked_execute:
        with mock.patch(
            "snowflake.core._internal.bridge.resources.database_resource.DatabaseResource.desc_db",
            side_effect=NotFound(),
        ):
            with pytest.raises(ServerError):
                dbs["new_db"].create_or_update(
                    Database(
                        name="new_db",
                        max_data_extension_time_in_days=1,
                    ),
                )
    mocked_execute.assert_called_once_with(
        "CREATE DATABASE NEW_DB MAX_DATA_EXTENSION_TIME_IN_DAYS = 1 "
    )

def test_create_or_update_update(fake_root):
    dbs = DatabaseCollection(fake_root)
    old_db = Database(
        name="db",
        comment="old comment",
        max_data_extension_time_in_days=0,
    )
    with mock.patch(
        "snowflake.core._internal.bridge.executor.SnowExecute.execute"
    ) as mocked_execute:
        with mock.patch(
            "snowflake.core._internal.bridge.resources.database_resource.DatabaseResource.desc_db",
            return_value=("fake sql", old_db.to_dict()),
        ):
            with pytest.raises(ServerError):
                dbs["db"].create_or_update(
                    Database(
                        name="db",
                        comment="new comment",
                        max_data_extension_time_in_days=1,
                    ),
                )
    mocked_execute.assert_called_once_with(
        "ALTER DATABASE DB SET comment = 'new comment' max_data_extension_time_in_days = 1"
    )


def test_create_from_share(fake_root):
    dbs = DatabaseCollection(fake_root)
    with mock.patch(
        "snowflake.core._internal.bridge.executor.SnowExecute.execute"
    ) as mocked_execute:
        with pytest.raises(ServerError):
            dbs._create_from_share(
                name="my_own_db",
                share="share.db",
            )
    mocked_execute.assert_called_once_with(
        "CREATE DATABASE MY_OWN_DB FROM SHARE share.db "
    )

def test_delete(fake_root):
    dbs = DatabaseCollection(fake_root)
    with mock.patch(
        "snowflake.core._internal.bridge.executor.SnowExecute.execute"
    ) as mocked_execute:
        with pytest.raises(ServerError):
            dbs["my_db"].delete()
    mocked_execute.assert_called_once_with(
        "DROP DATABASE MY_DB"
    )

def test_enable_replication(fake_root):
    dbs = DatabaseCollection(fake_root)
    with mock.patch(
        "snowflake.core._internal.bridge.executor.SnowExecute.execute"
    ) as mocked_execute:
        with pytest.raises(ServerError):
            dbs["my_db"].enable_replication(
                accounts=["my_org.account2"],
            )
    mocked_execute.assert_called_once_with(
        "ALTER DATABASE MY_DB ENABLE REPLICATION TO ACCOUNTS my_org.account2",
    )

def test_disable_replication(fake_root):
    dbs = DatabaseCollection(fake_root)
    with mock.patch(
        "snowflake.core._internal.bridge.executor.SnowExecute.execute"
    ) as mocked_execute:
        with pytest.raises(ServerError):
            dbs["my_db"].disable_replication(
                accounts=["my_org.account2"],
            )
    mocked_execute.assert_called_once_with(
        "ALTER DATABASE MY_DB DISABLE REPLICATION TO ACCOUNTS my_org.account2",
    )

def test_refresh_replication(fake_root):
    dbs = DatabaseCollection(fake_root)
    with mock.patch(
        "snowflake.core._internal.bridge.executor.SnowExecute.execute"
    ) as mocked_execute:
        with pytest.raises(ServerError):
            dbs["my_db"].refresh_replication()
    mocked_execute.assert_called_once_with(
        "ALTER DATABASE MY_DB REFRESH",
    )

def test_enable_failover(fake_root):
    dbs = DatabaseCollection(fake_root)
    with mock.patch(
        "snowflake.core._internal.bridge.executor.SnowExecute.execute"
    ) as mocked_execute:
        with pytest.raises(ServerError):
            dbs["my_db"].enable_failover(
                accounts=["my_org.account2"],
            )
    mocked_execute.assert_called_once_with(
        "ALTER DATABASE MY_DB ENABLE FAILOVER TO ACCOUNTS my_org.account2",
    )

def test_disable_failover(fake_root):
    dbs = DatabaseCollection(fake_root)
    with mock.patch(
        "snowflake.core._internal.bridge.executor.SnowExecute.execute"
    ) as mocked_execute:
        with pytest.raises(ServerError):
            dbs["my_db"].disable_failover()
    mocked_execute.assert_called_once_with(
        "ALTER DATABASE MY_DB DISABLE FAILOVER ",
    )

def test_promote_to_primary_failover(fake_root):
    dbs = DatabaseCollection(fake_root)
    with mock.patch(
        "snowflake.core._internal.bridge.executor.SnowExecute.execute"
    ) as mocked_execute:
        with pytest.raises(ServerError):
            dbs["my_db"].promote_to_primary_failover()
    mocked_execute.assert_called_once_with(
        "ALTER DATABASE MY_DB PRIMARY",
    )

def test_empty_alter(fake_root):
    dbs = DatabaseCollection(fake_root)
    with \
    mock.patch(
        "snowflake.core._internal.bridge.executor.SnowExecute.execute"
    ) as mocked_execute, \
    mock.patch(
        "snowflake.core._internal.bridge.resources.database_resource.DatabaseResource.desc_db",
        return_value=(None, {"name": "MY_DB", "comment": "a"}),
    ):
        dbs["my_db"].create_or_update(
            database=Database(name="MY_DB", comment="a"),
        )
    mocked_execute.assert_not_called()
