from django.urls import path
from api.views import ProductViewSet, SellerProductViewSet, CartViewSet


urlpatterns = [
    path(
        "buyer/products/",
        ProductViewSet.as_view({"get": "list"}),
        name="buyer_list_all_products",
    ),
    path(
        "buyer/products/<int:pk>/",
        ProductViewSet.as_view({"get": "retrieve"}),
        name="buyer_get_product",
    ),
    path(
        "seller/products/",
        SellerProductViewSet.as_view({"get": "list"}, name="seller_get_products"),
    ),
    path(
        "seller/products/create/",
        SellerProductViewSet.as_view({"post": "create"}, name="seller_create_products"),
    ),
    path(
        "seller/products/<int:pk>/",
        SellerProductViewSet.as_view(
            {"patch": "partial_update", "delete": "delete"},
            name="seller_update_or_delete_products",
        ),
    ),
    path(
        "buyer/cart/",
        CartViewSet.as_view({"get": "list", "post": "create"}),
    ),
    path(
        "buyer/cart/<int:pk>/",
        CartViewSet.as_view(
            {"patch": "partial_update", "delete": "delete"},
            name="seller_update_or_delete_products",
        ),
    ),
]
