from rest_framework.exceptions import APIException
from rest_framework import status

class CustomAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'A custom application error occurred.'
    default_code = 'custom_error'

class InsufficientStockError(CustomAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Insufficient stock available'
    default_code = 'insufficient_stock'

class InvalidStateTransitionError(CustomAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid state transition'
    default_code = 'invalid_state_transition'

class IdempotencyError(CustomAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Idempotency error'
    default_code = 'idempotency_error'

class OrderNotCancellableError(CustomAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Order not cancellable'
    default_code = 'order_not_cancellable'

