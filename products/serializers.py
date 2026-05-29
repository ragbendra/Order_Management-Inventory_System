from rest_framework import serializers
from .models import Warehouse, Inventory, Product

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta():
        model = Warehouse
        fields = ['id', 'name', 'location']

class InventorySerializer(serializers.ModelSerializer):
    class Meta():
        model = Inventory
        fields = ['available_qty', 'reserved_qty', 'low_stock_thresold']

class ProductSerializer(serializers.ModelSerializer):
    inventory = InventorySerializer(read_only=True)
    warehouse = WarehouseSerializer(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'sku', 'unit_price', 'description', 'warehouse', 'inventory', 'created_at', 'updated_at']