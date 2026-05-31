from django.db import transaction
import threading
from django.utils import timezone
from django_q.tasks import schedule
from django_q.models import Schedule
from products.models import Product
from products.services import reserve_stock, release_stock
from common.exceptions import IdempotencyError, OrderNotCancellableError
from .models import Order, OrderItem
from .state_machine import transition

def create_order(user, items, idempotency_key):
    # Check if order with same idempotency_key exists, return it if yes
    existing_order = Order.objects.filter(idempotency_key=idempotency_key).first()
    if existing_order:
        return existing_order

    with transaction.atomic():
        # Create Order record
        order = Order.objects.create(
            user=user,
            status=Order.StatusChoices.PENDING,
            idempotency_key=idempotency_key,
            total_amount=0.00
        )

        total_amount = 0
        for item in items:
            product_id = item['product_id']
            quantity = item['quantity']

            # Call reserve_stock() for each item
            reserve_stock(product_id=product_id, qty=quantity)

            # Retrieve product price
            product = Product.objects.get(pk=product_id)
            price = product.unit_price

            # Create OrderItem records for each item storing current product price as unit_price
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=price
            )
            # Calculate total_amount
            total_amount += price * quantity

        # Save total_amount
        order.total_amount = total_amount
        order.save()

        # Transition order state to PENDING (it is already created as PENDING, saving it fulfills state)
        order.status = Order.StatusChoices.PENDING
        order.save()

        # Trigger order confirmation notification in background using threading.Thread
        threading.Thread(target=send_order_confirmation, args=(order.id,)).start()

        # Schedule auto-cancel Django-Q2 task with 15 minute delay
        schedule(
            'orders.services.auto_cancel_order',
            order.id,
            schedule_type=Schedule.ONCE,
            next_run=timezone.now() + timezone.timedelta(minutes=15)
        )

    return order

def cancel_order(order_id):
    # Fetch order
    order = Order.objects.get(pk=order_id)

    # Check it is in a cancellable state (PENDING)
    if order.status != Order.StatusChoices.PENDING:
        raise OrderNotCancellableError(f"Order {order_id} is in status {order.status} and cannot be cancelled.")

    # Wrap in transaction.atomic()
    with transaction.atomic():
        # Call release_stock() for each order item
        for item in order.items.all():
            release_stock(product_id=item.product.id, qty=item.quantity)

        # Transition order state to CANCELLED
        transition(order, Order.StatusChoices.CANCELLED)

def auto_cancel_order(order_id):
    try:
        order = Order.objects.get(pk=order_id)
        if order.status == Order.StatusChoices.PENDING:
            cancel_order(order_id)
    except Order.DoesNotExist:
        pass

def send_order_confirmation(order_id):
    # Background order confirmation notification placeholder
    print(f"Sending order confirmation for Order ID: {order_id}")