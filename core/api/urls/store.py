# store/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import ProductViewSet, CartViewSet, SellerProductViewSet


router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="products")
router.register(r"cart", CartViewSet, basename="cart")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "seller/products/",
        SellerProductViewSet.as_view({"get": "list"}, name="seller_get_products"),
    ),
    path(
        "seller/products/create/",
        SellerProductViewSet.as_view({"post": "create"}, name="seller_create_products"),
    ),
]
