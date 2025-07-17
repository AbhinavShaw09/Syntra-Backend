from django.urls import path
from api.views import SellerProductViewSet, CartViewSet


urlpatterns = [
    path(
        "products/",
        SellerProductViewSet.as_view({"get": "list"}, name="seller_get_products"),
    ),
    path(
        "products/create/",
        SellerProductViewSet.as_view({"post": "create"}, name="seller_create_products"),
    ),
    path(
        "products/<int:pk>/",
        SellerProductViewSet.as_view(
            {"patch": "partial_update", "delete": "delete"},
            name="seller_update_or_delete_products",
        ),
    ),
]
