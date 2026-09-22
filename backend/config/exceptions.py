"""
TalentSphere Enterprise Custom API Exception Handler
Standardizes error payloads across all DRF views and endpoints.
Format:
{
    "success": false,
    "message": "Error detail message",
    "error_code": "ERROR_CODE_SLUG"
}
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        error_code = "API_ERROR"
        message = "An error occurred while processing your request."

        if response.status_code == 401:
            error_code = "UNAUTHORIZED"
            message = "Authentication credentials were not provided or are invalid."
        elif response.status_code == 403:
            error_code = "PERMISSION_DENIED"
            message = "You do not have permission to access this resource."
        elif response.status_code == 404:
            error_code = "NOT_FOUND"
            message = "The requested resource was not found."
        elif response.status_code == 429:
            error_code = "TOO_MANY_REQUESTS"
            message = "Rate limit exceeded. Please try again later."
        elif response.status_code == 400:
            error_code = "VALIDATION_ERROR"
            if isinstance(response.data, dict):
                message = response.data.get("detail", response.data)
            else:
                message = response.data

        response.data = {
            "success": False,
            "message": message,
            "error_code": error_code,
            "details": response.data if response.status_code == 400 and isinstance(response.data, dict) else None
        }

    return response
