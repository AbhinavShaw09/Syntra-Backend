from django.urls import path
from api.views import OrderViewSet

urlpatterns = [
    path(
        "orders/",
        OrderViewSet.as_view({"get": "list", "post": "create"}),
        name="orders",
    ),
    path(
        "orders/<int:pk>/",
        OrderViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
        name="order-detail",
    ),
    path(
        "orders/all/",
        OrderViewSet.as_view({"get": "get_all_seller_orders"}),
        name="all-seller-orders",
    ),
]
