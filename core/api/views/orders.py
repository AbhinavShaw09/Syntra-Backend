from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    OrderStatusUpdateSerializer,
)
from api.services import OrderService


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderService.get_user_orders(self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        elif self.action == "update":
            return OrderStatusUpdateSerializer
        return OrderSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(*args, **kwargs)
        return serializer

    def get_response_serializer(self, *args, **kwargs):
        serializer = OrderSerializer(*args, **kwargs)
        return serializer

    def list(self, request):
        orders = self.get_queryset()
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            order = serializer.save()
            response_serializer = self.get_response_serializer(order)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        order = OrderService.get_order_by_id(user_id=request.user.id, order_id=pk)
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    def update(self, request, pk=None):
        order = OrderService.get_order_by_id(user_id=request.user.id, order_id=pk)
        serializer = self.get_serializer(
            order, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            updated_order = serializer.save()
            response_serializer = self.get_response_serializer(
                updated_order, partial=True
            )
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_all_seller_orders(self, request):
        orders = OrderService.get_all_seller_orders()
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
