from django.db import models
from .base import BasePaymentModel


class OrderPaymentRequest(BasePaymentModel):
    class PaymentStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    order_id = models.PositiveIntegerField(unique=True, db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="USD")
    status = models.CharField(
        max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    payment_url = models.URLField(blank=True, null=True)
    third_party_data = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name = "Order Payment Request"
        verbose_name_plural = "Order Payment Requests"

    def __str__(self):
        return f"Payment Request for Order {self.order_id} - Status: {self.status}"


class PaymentWebhookEvent(BasePaymentModel):
    class EventType(models.TextChoices):
        PAYMENT_SUCCESS = "payment_success", "Payment Success"
        PAYMENT_FAILURE = "payment_failed", "Payment Failed"
        PAYMENT_PENDING = "payment_pending", "Payment Pending"

    order_id = models.PositiveIntegerField(db_index=True)
    transaction_id = models.CharField(max_length=100, unique=True)
    event_type = models.CharField(max_length=20, choices=EventType.choices)
    data = models.JSONField()

    class Meta:
        verbose_name = "Payment Webhook Event"
        verbose_name_plural = "Payment Webhook Events"

    def __str__(self):
        return f"Webhook Event {self.event_type} for Order {self.order_id}"
