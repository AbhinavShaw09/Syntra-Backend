from django.urls import path, include
from .accounts import urlpatterns as accounts_urls
from .store import urlpatterns as store_urls
from .orders import urlpatterns as order_urls
from .buyer import urlpatterns as buyer_urls
from .discounts import urlpatterns as discount_urls

urlpatterns = []

urlpatterns += [
    path("seller/", include(store_urls)),
    path("seller/", include(order_urls)),
    path("seller/", include(discount_urls)),
    path("buyer/", include(buyer_urls)),
    path("auth/", include(accounts_urls)),
]
