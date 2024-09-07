from utils.app_util import AppUtil


class TestAppUtil:
    _id = "848a3cdd-cafd-4ec6-a921-afb0bcc841dd"

    def test_validate_uuid4(self):
        actual_result = AppUtil.validate_uuid4(self._id)

        assert actual_result == True

    def test_validate_uuid4_invalid_uuid(self):
        actual_result = AppUtil.validate_uuid4("848a3cdd")

        assert actual_result == False

    async def test_get_app_version(self):
        actual_result = AppUtil.get_app_version()

        assert actual_result == "0.1.0"

    def test_validate_uuid_path_param_users_success(self):
        path_prefix = "/api/users/"
        request_path = path_prefix + self._id

        actual_result = AppUtil.validate_uuid_path_param(
            request_path, path_prefix, self._id
        )

        assert actual_result == True

    def test_validate_uuid_path_param_invalid_users(self):
        path_prefix = "/api/users/"
        request_path = path_prefix + "eaf0bb67-288b-4e56-860d-e727b4f57ff"

        actual_result = AppUtil.validate_uuid_path_param(
            request_path, path_prefix, self._id
        )

        assert actual_result == False

    def test_validate_uuid_path_param_user_details_success(self):
        path_prefix = "/api/user-details/"
        request_path = path_prefix + self._id

        actual_result = AppUtil.validate_uuid_path_param(
            request_path, path_prefix, self._id
        )

        assert actual_result == True

    def test_validate_uuid_path_param_invalid_user_details(self):
        path_prefix = "/api/user-details/"
        request_path = path_prefix + "eaf0bb67-288b-4e56-860d-e727b4f57ff"

        actual_result = AppUtil.validate_uuid_path_param(
            request_path, path_prefix, self._id
        )

        assert actual_result == False
