"""
Audit Log Middleware Placeholder for TalentSphere Phase 1.
Will be fully implemented in Phase 9.
"""

class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
