from django.urls import path
from api.views import OrderViewSet

urlpatterns = [
    path(
        "buyer/order/",
        OrderViewSet.as_view({"post": "create", "get": "retrieve_all_buyer_orders"}),
        name="order-create",
    ),
    path(
        "buyer/order/<int:pk>/",
        OrderViewSet.as_view({"get": "retrieve"}),
        name="order-detail",
    ),
    path(
        "seller/order/",
        OrderViewSet.as_view({"get": "list"}),
        name="buyer-order-list",
    ),
    path(
        "seller/order/<int:pk>/",
        OrderViewSet.as_view({"post": "update"}),
        name="buyer-order-list",
    ),
]
