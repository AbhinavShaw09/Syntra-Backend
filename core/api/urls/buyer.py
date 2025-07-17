from django.urls import path
from api.views import (
    BuyerAddressViewsSet,
    OrderViewSet,
    ProductViewSet,
    CartViewSet,
    BuyerAccountDetailsViewSet,
)

urlpatterns = [
    # Buyer Address urls
    path(
        "address/",
        BuyerAddressViewsSet.as_view({"get": "list"}),
        name="buyer_get_addresses",
    ),
    path(
        "address/create/",
        BuyerAddressViewsSet.as_view({"post": "create"}),
        name="buyer_create_addresses",
    ),
    path(
        "address/update/",
        BuyerAddressViewsSet.as_view({"put": "update"}),
        name="buyer_update_address",
    ),
    path(
        "address/delete/",
        BuyerAddressViewsSet.as_view({"delete": "delete"}),
        name="buyer_delete_address",
    ),
    # Order urls
    path(
        "order/",
        OrderViewSet.as_view({"post": "create", "get": "retrieve_all_buyer_orders"}),
        name="order-create",
    ),
    path(
        "order/<int:pk>/",
        OrderViewSet.as_view({"get": "retrieve"}),
        name="order-detail",
    ),
    # Product urls
    path(
        "products/",
        ProductViewSet.as_view({"get": "list"}),
        name="buyer_list_all_products",
    ),
    path(
        "products/<int:pk>/",
        ProductViewSet.as_view({"get": "retrieve"}),
        name="buyer_get_product",
    ),
    # Cart urls
    path(
        "cart/",
        CartViewSet.as_view({"get": "list", "post": "create"}),
    ),
    path(
        "cart/<int:pk>/",
        CartViewSet.as_view(
            {"patch": "partial_update", "delete": "delete"},
            name="seller_update_or_delete_products",
        ),
    ),
    # Buyer Account Details urls
    path(
        "account/details/",
        BuyerAccountDetailsViewSet.as_view(
            {"get": "retrieve", "post": "partial_update"}
        ),
    ),
]
