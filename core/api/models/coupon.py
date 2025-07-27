from django.db import models

from .account import User
from .store import Product
from .base import BaseModel


class Counpon(BaseModel):
    class CouponType(models.TextChoices):
        PERCENTAGE = "percentage", "Percentage"
        FIXED_AMOUNT = "fixed_amount", "Fixed Amount"

    code = models.CharField(max_length=50, unique=True)
    coupon_type = models.CharField(
        max_length=20, choices=CouponType.choices, default=CouponType.PERCENTAGE
    )
    value = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    max_usage_per_user = models.PositiveIntegerField(default=1)
    max_total_usage = models.PositiveIntegerField(default=1)
    total_usage_count = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return super().__str__()

    @property
    def get_user_usage_count(self, user_id):
        return UserCouponAppliedMapping.objects.filter(
            user_id=user_id, coupon=self
        ).count()


class UserCouponAppliedMapping(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_coupons"
    )
    coupon = models.ForeignKey(
        Counpon, on_delete=models.CASCADE, related_name="coupon_users"
    )
    usage_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("user", "coupon")

    def __str__(self):
        return f"{self.user.username} - {self.coupon.code} ({self.usage_count})"


class ProductCouponMapping(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_coupons"
    )
    coupon = models.ForeignKey(
        Counpon, on_delete=models.CASCADE, related_name="coupon_products"
    )

    class Meta:
        unique_together = ("product", "coupon")

    def __str__(self):
        return f"{self.product.name} - {self.coupon.code}"
