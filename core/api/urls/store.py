# store/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import ProductViewSet, CartViewSet

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="products")
router.register(r"cart", CartViewSet, basename="cart")

urlpatterns = [
    path("", include(router.urls)),
]
