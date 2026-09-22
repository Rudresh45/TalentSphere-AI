"""
TalentSphere Security & Audit Logging Middleware
Automatically captures system mutations and sensitive resource access.
"""
from audit_logs.models import AuditLog, AuditAction


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Log mutating actions (POST, PUT, PATCH, DELETE) and auth/payroll actions
        path = request.path
        if path.startswith('/api/v1/'):
            method = request.method
            if method in ['POST', 'PUT', 'PATCH', 'DELETE'] or 'payroll' in path or 'login' in path:
                user = request.user if request.user and request.user.is_authenticated else None
                username = user.username if user else 'Anonymous'

                action = AuditAction.UPDATE
                if 'login' in path:
                    action = AuditAction.LOGIN if response.status_code == 200 else AuditAction.FAILED_LOGIN
                elif 'logout' in path:
                    action = AuditAction.LOGOUT
                elif 'payroll' in path:
                    action = AuditAction.PAYROLL_ACCESS
                elif 'role' in path:
                    action = AuditAction.ROLE_CHANGE
                elif method == 'POST':
                    action = AuditAction.CREATE
                elif method == 'DELETE':
                    action = AuditAction.DELETE

                resource = path.strip('/').split('/')[2] if len(path.strip('/').split('/')) > 2 else 'api'

                try:
                    AuditLog.objects.create(
                        user=user,
                        username=username,
                        action=action,
                        resource=resource,
                        resource_id=path.split('/')[-2] if path.endswith('/') and len(path.split('/')) > 3 else None,
                        ip_address=get_client_ip(request),
                        request_method=method,
                        status_code=response.status_code,
                        details={"path": path}
                    )
                except Exception:
                    # Audit logging must never fail the primary request execution
                    pass

        return response
