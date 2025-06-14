from dataclasses import dataclass
from django.db import transaction
from django.conf import settings

from api.models import Product, OrderPaymentRequest, Order, PaymentWebhookEvent
from .payments_services.razorpay import RazorpayPaymentService

from api.services.order import OrderService


@dataclass
class PaymentRequestData:
    product_id: int
    amount: float
    currency: str = "INR"
    status: str = OrderPaymentRequest.Status.PENDING
    additional_data: dict = None
    url: str = None


class CorePaymentProviderService:
    PAYMENT_PROVIDER_SERVICE_MAP = {
        "razorpay": RazorpayPaymentService,
    }

    def __init__(self, payment_provider: str):
        if payment_provider not in self.PAYMENT_PROVIDER_SERVICE_MAP:
            raise ValueError(f"Payment provider '{payment_provider}' is not supported.")

        self.payment_provider_service = self.PAYMENT_PROVIDER_SERVICE_MAP[
            payment_provider
        ]()

    @classmethod
    def create_payment_request(
        cls, total_amount: int, order_id: id, **kwargs
    ) -> PaymentRequestData:
        if not total_amount or not order_id:
            raise ValueError(
                "Product ID or Order ID is required to create a payment request."
            )

        order: Order = OrderService.get_order_by_id(order_id)

        if not order:
            raise ValueError(f"Order with ID {order_id} does not exist.")

        payment_request = cls._initiate_payment_request(
            total_amount, order=order, **kwargs
        )

        return PaymentRequestData(
            amount=payment_request.amount,
            currency=kwargs.get("currency", "INR"),
            status=OrderPaymentRequest.Status.PENDING,
            additional_data=kwargs.get("additional_data", {}),
            url=payment_request.payment_url,
        )

    def _initiate_payment_request(
        self, total_amount: int, order: Order, **kwargs
    ) -> OrderPaymentRequest:

        with transaction.atomic():
            payment_request_data = self.payment_provider_service.initiate_payment(
                amount=total_amount,
                currency=kwargs.get("currency", "INR"),
                **kwargs,
            )

            payment_request = OrderPaymentRequest.objects.get_or_create(
                order_id=order.id,
                amount=total_amount,
                currency=kwargs.get("currency", "INR"),
                status=OrderPaymentRequest.Status.PENDING,
                third_party_data=payment_request_data.third_party_data,
                payment_url=payment_request_data.url,
            )
        return payment_request
