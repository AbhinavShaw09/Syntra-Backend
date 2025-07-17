from api.tests.base import BaseAPITestCase

from api.utils.test_utils import generate_random_phone_number


class BuyerAccountDetailsIntegrationTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.client = self.get_auth_client()
        self.buyer_address.phone_number = generate_random_phone_number()
        self.buyer_address.save()

    def test_get_buyer_details(self):
        response = self.client.get(
            path="/api/buyer/account/details/", content_type="application/json"
        )
        self.assertSuccessReponse(response)

        self.assertIn("id", response.data)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)
        self.assertIn("first_name", response.data)
        self.assertIn("last_name", response.data)

    def test_update_buyer_details(self):
        data = {
            "first_name": "UpdatedFirstName",
            "last_name": "UpdatedLastName",
            "email": "update@gmail.com",
        }
        response = self.client.post(
            path="/api/buyer/account/details/",
            data=data,
            content_type="application/json",
        )
        self.assertSuccessReponse(response)

        self.assertEqual(response.data["email"], data["email"])
        self.assertEqual(response.data["first_name"], data["first_name"])
        self.assertEqual(response.data["last_name"], data["last_name"])
