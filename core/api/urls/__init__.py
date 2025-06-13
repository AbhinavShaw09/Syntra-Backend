# api/urls.py
from django.urls import path, include
from .accounts import urlpatterns as accounts_urls
from .store import urlpatterns as store_urls
from .orders import urlpatterns as order_urls

urlpatterns = []

urlpatterns += [
    path("", include(accounts_urls)),
    path("", include(store_urls)),
    path("", include(order_urls)),
]
