from dataclasses import dataclass
from django.db import transaction
from django.conf import settings

from api.models import OrderPaymentRequest, Order
from .payments_services.razorpay import RazorpayPaymentService


@dataclass
class PaymentRequestData:
    amount: float
    currency: str = "INR"
    status: str = OrderPaymentRequest.PaymentStatus.PENDING
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

    def create_payment_request(
        self, total_amount: float, order_id: id, **kwargs
    ) -> PaymentRequestData:
        additional_data = kwargs.get("additional_data", {})
        user_id = additional_data.get("user_id", None)
        if not total_amount or not order_id:
            raise ValueError(
                "Product ID or Order ID is required to create a payment request."
            )

        from api.services import OrderService

        order: Order = OrderService.get_order_by_id(user_id=user_id, order_id=order_id)

        if not order:
            raise ValueError(f"Order with ID {order_id} does not exist.")

        payment_request = self._initiate_payment_request(
            total_amount=total_amount, order=order, **kwargs
        )

        return PaymentRequestData(
            amount=payment_request.amount,
            currency=kwargs.get("currency", "INR"),
            status=OrderPaymentRequest.PaymentStatus.PENDING,
            additional_data=kwargs.get("additional_data", {}),
            url=payment_request.payment_url,
        )

    def _initiate_payment_request(
        self, total_amount: float, order: Order, **kwargs
    ) -> OrderPaymentRequest:
        with transaction.atomic():
            payment_request_data = self.payment_provider_service.initiate_payment(
                amount=total_amount,
                **kwargs,
            )

            payment_request, _ = OrderPaymentRequest.objects.get_or_create(
                order_id=order.id,
                amount=total_amount,
                currency=kwargs.get("currency", "INR"),
                status=OrderPaymentRequest.PaymentStatus.PENDING,
                third_party_data=payment_request_data.third_party_data,
                payment_url=payment_request_data.url,
            )
        return payment_request
