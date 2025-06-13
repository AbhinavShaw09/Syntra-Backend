from django.db import models

from .base import BaseModel
from .account import User


class Product(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory_count = models.PositiveIntegerField(default=0)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return self.name

    @property
    def is_in_stock(self):
        return self.inventory_count > 0


class CartItem(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart_items"
    )
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ["user", "product"]

    def __str__(self):
        return f"{self.user.username} - {self.product.name} x{self.quantity}"

    @property
    def total_price(self):
        return self.product.price * self.quantity
