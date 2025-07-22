from django.urls import path
from api.views import OrderViewSet

urlpatterns = [
    path(
        "order/<int:pk>/",
        OrderViewSet.as_view({"post": "update", "get" : "get_all_seller_orders"}),
        name="buyer-order-list",
    ),
]
