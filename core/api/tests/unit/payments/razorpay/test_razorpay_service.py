import httpretty
import json


from django.conf import settings
from api.tests.base import BaseAPITestCase
from api.services import RazorpayPaymentService, CorePaymentProviderService
from api.services import OrderService, CartService

from api.tests.mocks.payments.razorpay import (
    mock_razorpay_payment_link_generation_response,
)

class RazorpayPaymentServiceTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()

    @httpretty.activate
    def test_initiate_payment(self):
        # mock payment creation response from razorpay
        httpretty.register_uri(
            httpretty.POST,
            "https://api.razorpay.com/v1/payments_links/",
            body=json.dumps(mock_razorpay_payment_link_generation_response()),
            content_type="application/json",
            status=200,
        )

        payment_request_data = RazorpayPaymentService().initiate_payment(amount=100)
        self.assertTrue(hasattr(payment_request_data, "url"))