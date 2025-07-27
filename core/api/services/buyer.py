from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from rest_framework.generics import get_object_or_404

from api.models import BuyerAddress


class BuyerAddressService:
    @staticmethod
    def get_all_buyer_address(user_id=None) -> QuerySet[BuyerAddress]:
        return BuyerAddress.objects.filter(user_id=user_id).order_by("-created_at")

    @staticmethod
    def get_buyer_address(user_id=None) -> QuerySet[BuyerAddress]:
        return BuyerAddress.objects.filter(user_id=user_id).last()


class BuyerAccountDetailsService:
    @staticmethod
    def get_all_buyer_details(user_id=None) -> QuerySet[User]:
        return get_object_or_404(User, pk=user_id)
