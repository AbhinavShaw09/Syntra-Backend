from django.contrib.auth.models import User
from django.db.models import QuerySet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from api.models import BuyerAddress


class BuyerAddressViewsSet(viewsets):
    permission_classes = [IsAuthenticated]

    def get_queryset(self, user: User) -> QuerySet[BuyerAddress]:
        return BuyerAddress.objects.filter(user_id=user.id).order_by('-created_at')

    def create(self, request):
        pass
