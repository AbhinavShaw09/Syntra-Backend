from django.db import models

from .base import BaseModel
from .account import User
from .store import Product
from .buyer import BuyerAddress


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
