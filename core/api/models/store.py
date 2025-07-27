from django.db import models
from django.db.models import CheckConstraint, Q

from .base import BaseModel
from .account import User


class Product(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory_count = models.PositiveIntegerField(default=0)
    image_url = models.URLField(blank=True)
    image_url_list = models.JSONField(blank=True, default=list)

    def __str__(self):
        return self.name

    @property
    def is_in_stock(self):
        return self.inventory_count > 0


class ProductAttribute(BaseModel):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)
    quantity = models.FloatField()


class ProductAttributeMapping(BaseModel):
    product_attribute = models.ForeignKey(
        ProductAttribute, on_delete=models.CASCADE, related_name="attribute_mappings"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_attribute_mappings"
    )


class ProductReview(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_reviews"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_reviews"
    )
    review = models.CharField(max_length=500)
    rating = models.FloatField()

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(rating__gte=0) & Q(rating__lte=5), name="rating_range"
            )
        ]


class ProductCategory(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class ProducCategoryMapping(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="category_mappings"
    )
    category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, related_name="product_mappings"
    )

    class Meta:
        unique_together = ("product", "category")


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
        return self.product.selling_price * self.quantity
