from typing import List

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.models.orders import Order, OrderItem
from api.service.store import CartService


class OrderService:
    @staticmethod
    def get_user_orders(user) -> List[Order]:
        return Order.objects.filter(user=user).prefetch_related("items__product")

    @staticmethod
    def get_order_by_id(user, order_id: str) -> Order:
        return get_object_or_404(Order, id=order_id, user=user)

    @staticmethod
    @transaction.atomic
    def create_order_from_cart(user) -> Order:
        cart_items = CartService.get_user_cart(user)

        if not cart_items:
            raise serializers.ValidationError("Cart is empty")

        for cart_item in cart_items:
            if cart_item.quantity > cart_item.product.inventory_count:
                raise serializers.ValidationError(
                    f"Insufficient stock for {cart_item.product.name}. "
                    f"Available: {cart_item.product.inventory_count}, Requested: {cart_item.quantity}"
                )

        total_amount = sum(item.total_price for item in cart_items)

        order = Order.objects.create(user=user, total_amount=total_amount)

        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                unit_price=cart_item.product.price,
            )

            cart_item.product.inventory_count -= cart_item.quantity
            cart_item.product.save()

        cart_items.delete()

        return order

    @staticmethod
    def update_order_status(user, order_id: str, status: str) -> Order:
        order = OrderService.get_order_by_id(user, order_id)
        order.status = status
        order.save()
        return order
