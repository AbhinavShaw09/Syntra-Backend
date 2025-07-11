from django.urls import path
from api.views import BuyerAddressViewsSet

urlpatterns = [
    path(
        "buyer/address/create/",
        BuyerAddressViewsSet.as_view({"post": "create"}),
        name="buyer_create_addresses",
    ),
    path(
        "buyer/address/",
        BuyerAddressViewsSet.as_view({"get": "list"}),
        name="buyer_get_addresses",
    ),
    path(
        "buyer/address/<int:pk>/update/",
        BuyerAddressViewsSet.as_view({"put": "update"}),
        name="buyer_update_address",
    ),
    path(
        "buyer/address/<int:pk>/delete/",
        BuyerAddressViewsSet.as_view({"delete": "delete"}),
        name="buyer_delete_address",
    ),
]
