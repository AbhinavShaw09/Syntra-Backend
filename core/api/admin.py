from django.contrib import admin
from .models import Seller, Buyer, Order, OrderItem, Product
# Register your models here.

admin.site.register(Seller)
admin.site.register(Buyer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Product)

