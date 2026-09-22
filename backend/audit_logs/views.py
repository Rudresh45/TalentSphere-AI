from rest_framework import viewsets, mixins
from audit_logs.models import AuditLog
from audit_logs.serializers import AuditLogSerializer
from accounts.permissions import IsHRAdmin


class AuditLogViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    Immutable Read-Only Audit Log API.
    Restricted to HR Admins and Super Admins.
    """
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsHRAdmin]
