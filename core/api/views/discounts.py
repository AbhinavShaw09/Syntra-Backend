from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.models import Coupon
from api.serializers.discounts import CouponSerializer

class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filter coupons by the logged-in user (seller) if needed, 
        # or just return all for now as per requirements.
        # Assuming this is for sellers to manage their coupons.
        return Coupon.objects.all()
