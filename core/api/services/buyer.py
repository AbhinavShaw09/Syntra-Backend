from django.db.models.query import QuerySet
from api.models import BuyerAddress


class BuyerAddressService:
    @staticmethod
    def get_all_buyer_address(user_id=None) -> QuerySet[BuyerAddress]:
        return BuyerAddress.objects.filter(user_id=user_id).order_by("-created_at")
