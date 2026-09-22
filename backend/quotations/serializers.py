from rest_framework import serializers
from quotations.models import Customer, Quotation, QuotationItem
from products.serializers import ProductSerializer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'name', 'email', 'phone', 'company_name', 'address', 'created_at')


class QuotationItemSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = QuotationItem
        fields = ('id', 'product', 'product_detail', 'quantity', 'unit_price', 'discount_percentage', 'line_total')


class QuotationSerializer(serializers.ModelSerializer):
    customer_detail = CustomerSerializer(source='customer', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    items = QuotationItemSerializer(many=True, read_only=True)

    class Meta:
        model = Quotation
        fields = (
            'id', 'quotation_number', 'customer', 'customer_detail',
            'created_by', 'created_by_name', 'status', 'subtotal',
            'discount_percentage', 'discount_amount', 'tax_amount',
            'grand_total', 'notes', 'valid_until', 'items', 'created_at', 'updated_at'
        )
