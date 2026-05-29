from django.db import transaction
from django.db.models import F
from .models import Inventory
from common.exceptions import InsufficientStockError

@transaction.atomic
def reserve_stock(product_id, qty):
    inventory = Inventory.objects.select_for_update().get(product_id=product_id)
    if inventory.available_qty < qty:
        raise InsufficientStockError()
    inventory.available_qty = F('available_qty') - qty
    inventory.reserved_qty = F('reserved_qty') + qty
    inventory.version = F('version') + 1
    inventory.save()
    
    
@transaction.atomic
def release_stock(product_id, qty):
    inventory = Inventory.objects.select_for_update().get(product_id=product_id)
    inventory.available_qty = F('available_qty') + qty
    inventory.reserved_qty = F('reserved_qty') - qty
    inventory.version = F('version') + 1
    inventory.save()


@transaction.atomic
def deduct_stock(product_id, qty):
    inventory = Inventory.objects.select_for_update().get(product_id=product_id)
    inventory.reserved_qty = F('reserved_qty') - qty
    inventory.version = F('version') + 1
    inventory.save()
     