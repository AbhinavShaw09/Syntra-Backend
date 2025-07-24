from django.urls import path
from api.views import SellerProductViewSet, SellerCategoryViewSet


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
            {"patch": "partial_update", "post": "delete_product"},
            name="seller_update_or_delete_products",
        ),
    ),
    path(
        "categories/",
        SellerCategoryViewSet.as_view(
            {"get": "list", "post": "create"}, name="seller_get_or_create_category"
        ),
    ),
    path(
        "categories/<int:pk>/",
        SellerCategoryViewSet.as_view(
            {"patch": "partial_update", "post": "delete_category"},
            name="seller_update_or_delete_category",
        ),
    ),
]
