from django.db import models

from .base import BaseModel
from .account import User


class BuyerAddress(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_address"
    )
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Buyer Addresse"
        verbose_name_plural = "Buyer Addresses"
