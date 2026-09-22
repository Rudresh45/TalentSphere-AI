from django.urls import path, include
from rest_framework.routers import DefaultRouter
from audit_logs.views import AuditLogViewSet

app_name = 'audit_logs'

router = DefaultRouter()
router.register(r'', AuditLogViewSet, basename='audit_log')

urlpatterns = [
    path('', include(router.urls)),
]
