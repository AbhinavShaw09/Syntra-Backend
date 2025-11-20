from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from api.models import Order, Product, Coupon

class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def stats(self, request):
        # Mock stats for now, or calculate real ones
        # In a real app, you'd filter by the seller's items
        total_orders = Order.objects.count()
        total_products = Product.objects.count()
        active_coupons = Coupon.objects.count()
        total_revenue = 0 # Calculate from orders
        
        return Response({
            "total_orders": total_orders,
            "total_products": total_products,
            "active_coupons": active_coupons,
            "total_revenue": total_revenue
        })
