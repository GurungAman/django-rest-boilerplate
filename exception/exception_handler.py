import traceback

from django.conf import settings
from django.http import JsonResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError


def custom_exception_handler(exc, context):
    drf_exception = exception_handler(exc, context)
    response = {"success": False, }
    if drf_exception is not None:
        # all errors with base type APIException will be handled here
        if isinstance(exc, ValidationError):
            response = handle_validation_errors(exc)
        else:
            response["message"] = exc.detail
            response["error"] = [{exc.get_codes(): exc.detail}]
        drf_exception.data = response
        return drf_exception

    if settings.DEBUG:
        print(traceback.format_exc())

    # respond with internal server error to all
    # exceptions except the ones defined by DRF
    return Response({
        "success": False,
        "message":  "Internal Server Error.",
        "error": [{
            f"{exc.__class__.__name__}": str(exc),
        }],
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def handle_validation_errors(error):
    response = {
        "success": False,
        "message": "Invalid data."
    }
    if isinstance(error.detail, (list, tuple)):
        response["errors"] = [{"error": error.detail[0]}]
    else:
        # ValidationError({"error": ["test error."]})
        error = {key: value[0]["message"]
                 for key, value in error.get_full_details().items()}
        response["error"] = [error]
    return response


def handle_404(request, exception):
    # this response is returned only when debug is False
    return JsonResponse({
        "success": False,
        "message":  "API endpoint not found.",
    }, status=status.HTTP_404_NOT_FOUND)
