from django.contrib.auth.models import User
from django.db.models import QuerySet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404

from api.models import BuyerAddress
from api.serializers import BuyerAddressSerializer

from api.services import BuyerAddressService

class BuyerAddressViewsSet(viewsets):
    permission_classes = [IsAuthenticated]
    serializer_class = BuyerAddressSerializer

    def get_queryset(self, user: User) -> QuerySet[BuyerAddress]:
        return BuyerAddressService.get_all_buyer_address()
    
    def list(self, request):
        buyer_address_data = self.get_queryset()
        serializer = self.serializer_class(data=buyer_address_data, many=True)
        return Response(data=serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data=serializer.validated_data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        buyer_address = get_object_or_404(BuyerAddress, pk=pk)
        serializer = self.serializer_class(
            buyer_address, data=request.data, partial=False
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        buyer_address = get_object_or_404(BuyerAddress, pk=pk)
        serializer = self.serializer_class(
            buyer_address, data=request.data, partial=False
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk=None):
        buyer_address = get_object_or_404(BuyerAddress, pk=pk)
        buyer_address.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
