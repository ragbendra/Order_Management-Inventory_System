from common.exceptions import InvalidStateTransitionError

VALID_TRANSITIONS = {
    'PENDING': ['CONFIRMED', 'CANCELLED'],
    'CONFIRMED': ['PROCESSING', 'REFUNDED'],
    'PROCESSING': ['SHIPPED'],
    'SHIPPED': ['DELIVERED'],
    'DELIVERED': ['REFUNDED'],
}

def transition(order, new_state):
    if new_state not in VALID_TRANSITIONS.get(order.status, []):
        raise InvalidStateTransitionError(f"Invalid state transition from {order.status} to {new_state}")
    order.status = new_state
    order.save()
    return order