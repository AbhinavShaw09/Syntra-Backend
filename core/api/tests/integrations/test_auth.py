from api.tests.base import BaseAPITestCase
from api.utils.test_utils import (
    generate_random_username,
    generate_random_email,
    generate_random_password,
)


class AuthIntegrationTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.register_url = "/api/auth/register/"
        self.login_url = "/api/auth/login/"

    def test_user_registration(self):
        data = {
            "username": generate_random_username(),
            "email": generate_random_email(),
            "password": generate_random_password(),
        }
        resp = self.client.post(
            self.register_url,
            data=data,
            content_type="application/json",
        )
        self.assertSuccessReponse(resp)
        self.assertIn("message", resp.data)

    def test_login_success(self):
        # Register first
        username = generate_random_username()
        email = generate_random_email()
        password = generate_random_password()

        registration_data = {
            "username": username,
            "email": email,
            "password": password,
        }
        resp = self.client.post(
            self.register_url,
            data=registration_data,
            content_type="application/json",
        )
        self.assertSuccessReponse(resp)
        self.assertIn("message", resp.data)

        # login flow
        login_data = {"username": username, "password": password}
        resp = self.client.post(
            self.login_url,
            data=login_data,
            content_type="application/json",
        )
        self.assertSuccessReponse(resp)
        self.assertIn("access_token", resp.data)

    def test_login_invalid_credentials(self):
        data = {"username": self.username, "password": "wrongpassword"}
        resp = self.client.post(
            self.login_url,
            data=data,
            content_type="application/json",
        )
        self.assertErrorResponse(resp)
