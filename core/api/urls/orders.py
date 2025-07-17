from django.urls import path
from api.views import OrderViewSet

urlpatterns = [
    path(
        "order/",
        OrderViewSet.as_view({"get": "list"}),
        name="buyer-order-list",
    ),
    path(
        "order/<int:pk>/",
        OrderViewSet.as_view({"post": "update"}),
        name="buyer-order-list",
    ),
]
