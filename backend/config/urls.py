"""
TalentSphere Master API URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # OpenAPI 3 Schema & Swagger UI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Modular API Version 1 Endpoints
    path('api/v1/auth/', include('accounts.urls')),
    path('api/v1/departments/', include('departments.urls')),
    path('api/v1/employees/', include('employees.urls')),
    path('api/v1/recruitment/', include('recruitment.urls')),
    path('api/v1/attendance/', include('attendance.urls')),
    path('api/v1/payroll/', include('payroll.urls')),
    path('api/v1/onboarding/', include('onboarding.urls')),
    path('api/v1/offboarding/', include('offboarding.urls')),
    path('api/v1/projects/', include('projects.urls')),
    path('api/v1/tasks/', include('tasks.urls')),
    path('api/v1/sprints/', include('sprints.urls')),
    path('api/v1/performance/', include('performance.urls')),
    path('api/v1/quotations/', include('quotations.urls')),
    path('api/v1/products/', include('products.urls')),
    path('api/v1/ai/', include('ai_intelligence.urls')),
    path('api/v1/audit-logs/', include('audit_logs.urls')),
]
