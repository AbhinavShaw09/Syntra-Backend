from django.contrib.auth.models import User
from django.db.models import QuerySet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status


from api.models import BuyerAddress
from api.serializers import BuyerAddressSerializer, BuyerAccountDetailsSerializer

from api.services import BuyerAddressService, BuyerAccountDetailsService


class BuyerAddressViewsSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BuyerAddressSerializer

    def get_queryset(self, user_id: int) -> QuerySet[BuyerAddress]:
        return BuyerAddressService.get_all_buyer_address(user_id=user_id)

    def list(self, request):
        buyer_address_data = self.get_queryset(request.auth.get("user_id"))
        serializer = self.serializer_class(instance=buyer_address_data, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data=serializer.validated_data, status=status.HTTP_201_CREATED)

    def update(self, request):
        buyer_address = BuyerAddressService.get_buyer_address(
            user_id=request.auth.get("user_id")
        )
        serializer = self.serializer_class(
            buyer_address, data=request.data, partial=False
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=request.user)
        return Response(serializer.data)

    def delete(self, request):
        buyer_address = BuyerAddressService.get_buyer_address(
            user_id=request.auth.get("user_id")
        )
        buyer_address.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BuyerAccountDetailsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request):
        user_id = request.auth.get("user_id")
        user = BuyerAccountDetailsService.get_all_buyer_details(user_id=user_id)
        serializer = BuyerAccountDetailsSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request):
        user_id = request.auth.get("user_id")
        user = BuyerAccountDetailsService.get_all_buyer_details(user_id=user_id)
        serializer = BuyerAccountDetailsSerializer(
            user, data=request.data, partial=True, context={"request": request}
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
