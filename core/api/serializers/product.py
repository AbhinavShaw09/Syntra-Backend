from rest_framework import serializers
from api.models import Product, ProductCategory, ProductCategoryMapping


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(
        required=False, max_length=500, default="", allow_blank=True
    )
    original_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    selling_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    inventory_count = serializers.IntegerField()
    image_url = serializers.URLField(required=False, allow_blank=True)
    image_url_list = serializers.JSONField(required=False)
    is_in_stock = serializers.BooleanField(read_only=True)
    category_id = serializers.IntegerField(write_only=True, required=False)
    categories = serializers.SerializerMethodField(read_only=True)

    def get_categories(self, obj):
        return [
            {"id": mapping.category.id, "name": mapping.category.name}
            for mapping in obj.category_mappings.select_related("category").all()
        ]

    def create(self, validated_data):
        category_id = validated_data.pop("category_id", None)
        product = Product.objects.create(**validated_data)
        
        if category_id:
            try:
                category = ProductCategory.objects.get(id=category_id)
                ProductCategoryMapping.objects.create(product=product, category=category)
            except ProductCategory.DoesNotExist:
                raise serializers.ValidationError({"category_id": "Invalid category ID"})
        
        return product

    def update(self, instance, validated_data):
        category_id = validated_data.pop("category_id", None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if category_id:
            try:
                category = ProductCategory.objects.get(id=category_id)
                ProductCategoryMapping.objects.get_or_create(
                    product=instance, category=category
                )
            except ProductCategory.DoesNotExist:
                raise serializers.ValidationError({"category_id": "Invalid category ID"})
        
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["in_stock"] = instance.is_in_stock
        return representation


class ProductCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(
        required=False, max_length=500, default="", allow_blank=True
    )
    image_url = serializers.URLField(required=False, allow_blank=True)

    def create(self, validated_data):
        return ProductCategory.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
