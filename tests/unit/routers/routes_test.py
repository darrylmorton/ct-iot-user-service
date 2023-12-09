import pytest

from src.main import server
from tests.helper.routes import mock_http_client


@pytest.mark.asyncio
async def test_health():
    response = await mock_http_client(server, "http://test", "healthz")

    assert response.status_code == 200
    assert response.json() == {"message": "ok"}