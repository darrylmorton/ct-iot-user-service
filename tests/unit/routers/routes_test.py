import config
from user_service.service import app
from tests.helper.routes_helper import mock_http_client


async def test_health():
    response = await mock_http_client(app, "http://test", "healthz")

    assert response.status_code == 200
    assert response.json() == {"message": "ok", "version": config.APP_VERSION}
