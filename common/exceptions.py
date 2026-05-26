from rest_framework.exceptions import APIException
from rest_framework import status

class CustomAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'A custom application error occurred.'
    default_code = 'custom_error'
