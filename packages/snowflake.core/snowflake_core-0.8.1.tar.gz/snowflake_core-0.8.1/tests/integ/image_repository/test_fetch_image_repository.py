#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#


import pytest

from snowflake.core.image_repository import ImageRepository


pytestmark = pytest.mark.usefixtures("use_rest")


def test_fetch(image_repositories, temp_ir):
    ir: ImageRepository = image_repositories[temp_ir.name].fetch()
    assert ir.name == temp_ir.name.upper()  # for upper/lower case names
    assert ir.created_on
    assert ir.repository_url
