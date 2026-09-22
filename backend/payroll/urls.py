from django.urls import path, include
from rest_framework.routers import DefaultRouter
from payroll.views import SalaryStructureViewSet, PayslipViewSet

app_name = 'payroll'

router = DefaultRouter()
router.register(r'structures', SalaryStructureViewSet, basename='salary_structure')
router.register(r'payslips', PayslipViewSet, basename='payslip')

urlpatterns = [
    path('', include(router.urls)),
]
