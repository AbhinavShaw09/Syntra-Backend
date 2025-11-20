from django.urls import path
from api.views.discounts import DiscountViewSet

urlpatterns = [
    path(
        "discounts/",
        DiscountViewSet.as_view({"get": "list", "post": "create"}),
        name="seller_get_or_create_discounts",
    ),
    path(
        "discounts/<int:pk>/",
        DiscountViewSet.as_view(
            {"patch": "partial_update", "delete": "destroy"},
            name="seller_update_or_delete_discounts",
        ),
    ),
]
