from typing import List

from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.models import Order, OrderItem, Buyer, BuyerAddress
from api.services.store import CartService
from api.services.payments.core import CorePaymentProviderService


class OrderService:
    ORDER_PAYMENT_SERVICE_PROVIDER = (
        settings.ORDER_PAYMENNT_SERVICE_PROVIDER or "razorpay"
    )

    @staticmethod
    def get_user_orders(user) -> List[Order]:
        return Order.objects.filter(user=user).prefetch_related("items__product")

    @staticmethod
    def get_order_by_id(user_id, order_id: str) -> Order:
        return get_object_or_404(Order, id=order_id, user_id=user_id)

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

        buyer = Buyer.objects.filter(user_id=user.id).first()
        if not buyer:
            raise serializers.ValidationError("Buyer does not exists")

        buyer_address = BuyerAddress.objects.filter(
            user_id=user.id, is_active=True
        ).first()
        if not buyer_address:
            raise serializers.ValidationError("Buyer Address does not exists")

        total_amount = sum(item.total_price for item in cart_items)

        order = Order.objects.create(
            user=user, total_amount=total_amount, buyer_address=buyer_address
        )

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

        if not settings.IN_TESTING:
            # Skipping payment link generation for now
            OrderService.create_payment_request_for_order(order)

        return order

    @staticmethod
    def create_payment_request_for_order(order: Order):
        CorePaymentProviderService(
            payment_provider=OrderService.ORDER_PAYMENT_SERVICE_PROVIDER
        ).create_payment_request(
            total_amount=order.total_amount,
            order_id=order.id,
            currency="INR",
            additional_data={
                "user_id": order.user.id,
                "order_id": order.id,
            },
        )

    @staticmethod
    def update_order_status(user, order_id: str, status: str) -> Order:
        order = OrderService.get_order_by_id(user, order_id)
        order.status = status
        order.save()
        return order
