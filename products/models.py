from django.db import models
from common.models import BaseModel
# Create your models here.

class Warehouse(BaseModel):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=150)

class Product(BaseModel):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=100, unique=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='products')

class Inventory(BaseModel):
    version = models.PositiveIntegerField(default=0)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name = 'inventory')
    available_qty = models.PositiveIntegerField(default=0)
    reserved_qty = models.PositiveIntegerField(default=0)
    low_stock_thresold = models.PositiveIntegerField(default=10)
    



