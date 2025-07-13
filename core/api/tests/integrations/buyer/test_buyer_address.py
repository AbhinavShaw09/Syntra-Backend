from api.tests.base import BaseAPITestCase
from api.models import BuyerAddress

from api.utils.test_utils import generate_random_phone_number


class BuyerAddressIntegrationTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.client = self.get_auth_client()
        self.buyer_address = self.make_model(BuyerAddress, user_id=self.user.id)
        self.buyer_address.phone_number = generate_random_phone_number()
        self.buyer_address.save()

    def get_buyer_payload(self):
        return {
            "first_name": self.buyer_address.first_name,
            "last_name": self.buyer_address.last_name,
            "phone_number": self.buyer_address.phone_number,
            "address_line1": self.buyer_address.address_line1,
            "address_line2": self.buyer_address.address_line2,
            "phone_number": self.buyer_address.phone_number,
            "city": self.buyer_address.city,
            "country": self.buyer_address.country,
        }

    def create_address(self):
        return self.client.post(
            "/api/buyer/address/create/",
            data=self.get_buyer_payload(),
            content_type="application/json",
        )

    def test_get_buyer_address(self):
        response = self.client.get(
            path="/api/buyer/address/", content_type="application/json"
        )
        self.assertSuccessReponse(response)
        self.assertEqual(len(response.data), 1)

        response = self.create_address()
        self.assertSuccessReponse(response)

        response = self.client.get(
            path="/api/buyer/address/", content_type="application/json"
        )
        self.assertSuccessReponse(response)
        self.assertEqual(len(response.data), 2)

    def test_create_buyer_address(self):
        response = self.create_address()
        self.assertEqual(response.status_code, 201)
        self.assertIn("first_name", response.data)
        self.assertEqual(response.data["first_name"], self.buyer_address.first_name)
        self.assertEqual(response.data["last_name"], self.buyer_address.last_name)
        self.assertEqual(response.data["phone_number"], self.buyer_address.phone_number)
        self.assertEqual(
            response.data["address_line1"], self.buyer_address.address_line1
        )
        self.assertEqual(
            response.data["address_line2"], self.buyer_address.address_line2
        )

    def test_update_buyer_address(self):
        response = self.create_address()
        self.assertEqual(response.status_code, 201)

        response = self.client.put(
            f"/api/buyer/address/{self.buyer_address.id}/update/",
            data=self.get_buyer_payload(),
            content_type="application/json",
        )
        self.assertSuccessReponse(response)

    def test_delete_buyer_address(self):
        response = self.create_address()
        self.assertEqual(response.status_code, 201)

        response = self.client.delete(
            f"/api/buyer/address/{self.buyer_address.id}/delete/",
            content_type="application/json",
        )
        self.assertSuccessReponse(response)
