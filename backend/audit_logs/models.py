from django.db import models
from django.conf import settings


class AuditAction(models.TextChoices):
    LOGIN = 'LOGIN', 'User Login'
    LOGOUT = 'LOGOUT', 'User Logout'
    FAILED_LOGIN = 'FAILED_LOGIN', 'Failed Login Attempt'
    CREATE = 'CREATE', 'Resource Created'
    UPDATE = 'UPDATE', 'Resource Updated'
    DELETE = 'DELETE', 'Resource Deleted'
    ROLE_CHANGE = 'ROLE_CHANGE', 'User Role Changed'
    PAYROLL_ACCESS = 'PAYROLL_ACCESS', 'Payroll Data Accessed'


class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    username = models.CharField(max_length=150, blank=True, null=True)
    action = models.CharField(max_length=30, choices=AuditAction.choices, db_index=True)
    resource = models.CharField(max_length=100, db_index=True)
    resource_id = models.CharField(max_length=50, blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    request_method = models.CharField(max_length=10)
    status_code = models.IntegerField(default=200)
    details = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['action', 'timestamp']),
            models.Index(fields=['resource', 'resource_id']),
        ]

    def __str__(self):
        return f"[{self.timestamp}] {self.username or 'Anon'} - {self.action} on {self.resource}"
