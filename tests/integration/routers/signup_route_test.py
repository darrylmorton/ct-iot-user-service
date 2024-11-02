import tests.config as test_config
from tests.helper.email_helper import create_sqs_queue
from tests.helper.user_helper import create_signup_payload
from tests.helper.routes_helper import RoutesHelper
from user_service.service import app


class TestSignupRoute:
    async def test_post_signup_invalid_username(self):
        _username = "foo"
        payload = create_signup_payload(_username=_username)

        response = await RoutesHelper.http_post_client(app, "/api/signup", payload)

        assert response.status_code == 400

    async def test_post_signup_invalid_password(self):
        payload = create_signup_payload(_password="barbarb")

        response = await RoutesHelper.http_post_client(app, "/api/signup", payload)

        assert response.status_code == 400

    async def test_post_signup(self, db_cleanup, email_producer):
        create_sqs_queue(
            queue_name=test_config.SQS_EMAIL_QUEUE_NAME,
            dlq_name=test_config.SQS_EMAIL_DLQ_NAME,
        )

        payload = create_signup_payload()

        response = await RoutesHelper.http_post_client(app, "/api/signup", payload)
        actual_result = response.json()

        assert response.status_code == 201
        assert actual_result["username"] == test_config.SES_TARGET

    async def test_post_signup_user_exists(self):
        payload = create_signup_payload()

        response = await RoutesHelper.http_post_client(app, "/api/signup", payload)

        assert response.status_code == 409
