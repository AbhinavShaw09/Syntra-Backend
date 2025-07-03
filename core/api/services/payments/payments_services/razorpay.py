import requests
from dataclasses import dataclass
from django.conf import settings
from typing import Optional
from ..base import BasePaymentService


@dataclass
class RazorpayPaymentRequestData:
    amount: float
    currency: str = "INR"
    status: str = "PENDING"
    additional_data: dict = None
    third_party_data: dict = None
    url: str = None


class RazorpayPaymentService(BasePaymentService):
    def __init__(self):
        self.client_id = settings.RAZORPAY_CLIENT_ID
        self.client_secret = settings.RAZORPAY_CLIENT_SECRET
        self.base_url = settings.RAZORPAY_BASE_URL

    def make_request(
        self, endpoint: str, payload: dict = {}, headers: Optional[dict] = None
    ) -> dict:
        headers = headers or {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        response = requests.post(
            f"{self.base_url}/{endpoint}",
            json=payload,
            headers=headers,
            auth=(self.client_id, self.client_secret),
        )

        resp = response.json()
        if "error" in resp:
            raise Exception(f"Razorpay API Error: {resp['error']['description']}")

        return resp

    def initiate_payment(
        self, amount, currency="INR", **kwargs
    ) -> RazorpayPaymentRequestData:
        payload = {
            "amount": float(amount * 100),
            "currency": currency,
            "notes": kwargs.get("notes", {}),
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        resp_data = self.make_request(
            "payments_links/", payload=payload, headers=headers
        )

        return RazorpayPaymentRequestData(
            amount=amount,
            currency=currency,
            status="created",
            additional_data=kwargs.get("additional_data", {}),
            third_party_data=resp_data,
            url=resp_data.get("short_url"),
        )

    def handle_webhook(self, data: dict) -> dict:
        super().handle_webhook(data)

    def get_payment_status_by_polling(self, transaction_id: str) -> dict:
        super().get_payment_status_by_polling(transaction_id)
