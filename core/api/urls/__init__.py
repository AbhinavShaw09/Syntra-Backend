# api/urls.py
from django.urls import path
from .accounts import urlpatterns as accounts_urls

urlpatterns = [
    
]
urlpatterns += accounts_urls