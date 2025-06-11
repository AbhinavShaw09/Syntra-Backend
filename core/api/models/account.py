from django.db import models
from django.contrib.auth.models import User

from .base import BaseModel

class Seller(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=10)  # assume +91 prefix

    def __str__(self):
        return f"Seller: {self.name} ({self.phone})"


class Buyer(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer_profile')
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=10)  # assume +91 prefix

    def __str__(self):
        return f"Buyer: {self.name} ({self.phone})"
