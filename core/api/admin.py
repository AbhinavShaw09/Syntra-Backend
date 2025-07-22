from django.contrib import admin
from .models import (
    Seller,
    Buyer,
    Order,
    BuyerAddress,
    OrderItem,
    Product,
    ProductAttribute,
    ProductAttributeMapping,
    OrderPaymentRequest,
    PaymentWebhookEvent,
    CartItem
)
# Register your models here.

admin.site.register(Seller)
admin.site.register(Buyer)
admin.site.register(Order)
admin.site.register(BuyerAddress)
admin.site.register(OrderItem)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(ProductAttribute)
admin.site.register(ProductAttributeMapping)
admin.site.register(OrderPaymentRequest)
admin.site.register(PaymentWebhookEvent)
