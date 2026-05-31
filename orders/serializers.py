from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total_amount', 'idempotency_key', 'items', 'created_at', 'updated_at']

class CreateOrderSerializer(serializers.Serializer):
    class ItemInputSerializer(serializers.Serializer):
        product_id = serializers.IntegerField(min_value=1)
        quantity = serializers.IntegerField(min_value=1)

    idempotency_key = serializers.CharField(max_length=255, required=True)
    items = ItemInputSerializer(many=True, allow_empty=False)
