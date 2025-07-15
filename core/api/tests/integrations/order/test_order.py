import httpretty
from rest_framework.response import Response
from api.tests.base import BaseAPITestCase

from api.tests.mocks.payments.razorpay import MockRazorPayRequests


class OrderIntegrationTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.client = self.get_auth_client()

    def create_order(self) -> Response:
        return self.client.post(
            path=f"/api/buyer/order/", content_type="application/json"
        )

    @httpretty.activate
    def test_get_buyer_orders(self):
        MockRazorPayRequests().mock_razorpay_requests()
        response = self.client.get(
            path=f"/api/buyer/order/", content_type="application/json"
        )
        self.assertSuccessReponse(response)
        self.assertNoDataInReponse(response)

        response = self.create_buyer_cart()
        self.assertSuccessReponse(response)

        response = self.create_order()
        self.assertSuccessReponse(response)

        response = self.client.get(
            path=f"/api/buyer/order/", content_type="application/json"
        )
        self.assertSuccessReponse(response)
        self.assertEqual(len(response.data), 1)
