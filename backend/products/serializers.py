from rest_framework import serializers
from products.models import ProductCategory, Product


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('id', 'name', 'description')


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'category', 'category_name', 'name', 'code', 'description', 'unit_price', 'tax_rate', 'is_active', 'created_at')
