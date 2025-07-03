import time
from api.utils.test_utils import random_razorpay_short_url


def mock_razorpay_payment_link_generation_response():
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
