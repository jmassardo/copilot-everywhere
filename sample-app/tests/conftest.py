from datetime import datetime, timedelta

import pytest


@pytest.fixture
def assert_utc_timestamp():
    def _assert_utc_timestamp(value):
        created_at = datetime.fromisoformat(value)
        assert created_at.tzinfo is not None
        assert created_at.utcoffset() == timedelta(0)

    return _assert_utc_timestamp
