from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Inventory
from django.core.cache import cache


@receiver(post_save, sender=Inventory)
def invalidate_product_cache(sender, instance, **kwargs):
    cache.delete('product_list')
    cache.delete(f'product_{instance.product_id}')

