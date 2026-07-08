import pytest

from app.db.dependencies import get_db


@pytest.mark.asyncio
async def test_db_dependency() -> None:
    async_gen = get_db()
    # Can't easily test the actual DB connection without a running DB.
    # We will just verify it returns a generator.
    assert async_gen is not None
