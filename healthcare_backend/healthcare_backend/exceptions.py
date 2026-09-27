"""
Central, consistent error-response formatting for the whole API.
Every error the client receives has the shape:
{
    "success": false,
    "message": "Human readable summary",
    "errors": {...}
}
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        error_payload = {
            "success": False,
            "message": _summarize(response.data),
            "errors": response.data,
        }
        response.data = error_payload
        return response

    # Unhandled exceptions -> generic 500, never leak stack traces
    return Response(
        {
            "success": False,
            "message": "Something went wrong on our end. Please try again.",
            "errors": {"detail": str(exc)},
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def _summarize(data):
    if isinstance(data, dict):
        if "detail" in data:
            return str(data["detail"])
        for value in data.values():
            if isinstance(value, list) and value:
                return str(value[0])
    if isinstance(data, list) and data:
        return str(data[0])
    return "Request failed validation."
