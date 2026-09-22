from rest_framework import serializers
from audit_logs.models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = (
            'id', 'user', 'username', 'action', 'resource', 'resource_id',
            'ip_address', 'request_method', 'status_code', 'details', 'timestamp'
        )
