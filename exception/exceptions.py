from rest_framework.exceptions import APIException
from rest_framework import status


class CustomApiError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('A server error occurred.')
    default_code = 'error_code'