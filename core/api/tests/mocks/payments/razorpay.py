import time
import json
import httpretty
from api.utils.test_utils import random_razorpay_short_url


class MockRazorPayRequests:
    def __init__(self):
        super().__init__()

    def mock_razorpay_requests(self, order_id=None):
        httpretty.register_uri(
            httpretty.POST,
            "https://api.razorpay.com/v1/payments_links/",
            body=json.dumps(self._mock_razorpay_payment_link_generation_response()),
            content_type="application/json",
            status=200,
        )

    def _mock_razorpay_payment_link_generation_response(self):
        return {
            "accept_partial": False,
            "amount": 10000,
            "amount_paid": 0,
            "cancelled_at": 0,
            "created_at": int(time.time()),
            "currency": "INR",
            "customer": [],
            "description": "",
            "expire_by": 0,
            "expired_at": 0,
            "first_min_partial_amount": 0,
            "id": "plink_QoPyuZwMfHzzrG",
            "notes": None,
            "notify": {"email": False, "sms": False, "whatsapp": False},
            "payments": False,
            "reference_id": "",
            "reminder_enable": False,
            "reminders": [],
            "short_url": random_razorpay_short_url(),
            "status": "created",
            "updated_at": int(time.time()),
            "upi_link": False,
            "user_id": "",
            "whatsapp_link": False,
        }
