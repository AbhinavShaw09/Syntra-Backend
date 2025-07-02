from django.db import models

from .base import BaseModel
from .account import User, Buyer
from .store import Product


class BuyerAddress(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_address"
    )
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Buyer Addresse"
        verbose_name_plural = "Buyer Addresses"


class Order(BaseModel):
    class StatusChoices(models.IntegerChoices):
        PENDING = (0,)
        PROCESSING = (1,)
        SHIPPED = (2,)
        DELIVERED = (3,)
        CANCELLED = (4,)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField(
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING.value,
    )
    buyer_address = models.ForeignKey(BuyerAddress, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order {str(self.id)[:8]} - {self.user.username}"


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_items"
    )
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.order} - {self.product.name} x{self.quantity}"

    @property
    def total_price(self):
        return self.unit_price * self.quantity
