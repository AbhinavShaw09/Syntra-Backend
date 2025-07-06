import httpretty
import json


from django.conf import settings
from api.tests.base import BaseAPITestCase
from api.services import RazorpayPaymentService

from api.tests.mocks.payments.razorpay import MockRazorPayRequests


class RazorpayPaymentServiceTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()

    @httpretty.activate
    def test_initiate_payment(self):
        # mock payment creation response from razorpay
        MockRazorPayRequests().mock_razorpay_requests()

        payment_request_data = RazorpayPaymentService().initiate_payment(amount=100)
        self.assertTrue(hasattr(payment_request_data, "url"))
