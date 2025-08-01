from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from api.serializers import (
    ProductSerializer,
    ProductCategorySerializer,
    CartItemSerializer,
    CartItemUpdateSerializer,
)
from api.services import ProductService, CartService
from api.models import Product, ProductCategory


class ProductViewSet(viewsets.ViewSet):
    permission_classes = []
    serializer_class = ProductSerializer

    def get_queryset(self):
        return ProductService.get_all_products()

    def list(self, request):
        product = self.get_queryset()
        serializer = self.serializer_class(product, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        product = ProductService.get_product_by_id(product_id=pk)
        serializer = self.serializer_class(product)
        return Response(serializer.data)


class SellerProductViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()

    def list(self, request):
        product_data = self.get_queryset()
        serializer = self.serializer_class(product_data, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(
            serializer.data,
        )

    def partial_update(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        serializer = self.serializer_class(product, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)

    def delete_product(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        product.soft_delete()
        return Response(status=status.HTTP_200_OK)


class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartService.get_user_cart(self.request.user)

    def get_serializer_class(self):
        if self.action == "update" or self.action == "partial_update":
            return CartItemUpdateSerializer
        return CartItemSerializer

    def list(self, request):
        cart_items = self.get_queryset()
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CartItemSerializer(
            data=request.data, context={"request": request}, many=True
        )
        if serializer.is_valid():
            cart_item = serializer.save()
            response_serializer = CartItemSerializer(cart_item, many=True)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, product_id=None):
        cart_item = CartService.get_cart_item(user=request.user, product_id=product_id)
        serializer = CartItemUpdateSerializer(
            cart_item, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            updated_cart_item = serializer.save()
            response_serializer = CartItemSerializer(updated_cart_item)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id=None):
        CartService.remove_from_cart(user=request.user, product_id=product_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SellerCategoryViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductCategorySerializer

    def get_queryset(self):
        return ProductCategory.objects.all()

    def list(self, request):
        product_category_data = self.get_queryset()
        serializer = self.serializer_class(product_category_data, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(
            serializer.data,
        )

    def partial_update(self, request, pk=None):
        product_category = get_object_or_404(ProductCategory, pk=pk)
        serializer = self.serializer_class(
            product_category, data=request.data, partial=True
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)

    def delete_category(self, request, pk=None):
        category = get_object_or_404(ProductCategory, pk=pk)
        category.soft_delete()
        return Response(status=status.HTTP_200_OK)
