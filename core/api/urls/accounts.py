from django.urls import path
from api.views import AuthViewSet

urlpatterns = [
    path("auth/register/", AuthViewSet.as_view({"post": "register"}), name="register"),
    path("auth/login/", AuthViewSet.as_view({"post": "login"}), name="login"),
]
