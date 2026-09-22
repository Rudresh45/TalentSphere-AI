from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from payroll.models import SalaryStructure, Payslip
from payroll.serializers import SalaryStructureSerializer, PayslipSerializer
from accounts.permissions import IsFinance, IsHRAdmin
from accounts.models import UserRole
from employees.selectors import get_employee_by_user_id


class SalaryStructureViewSet(viewsets.ModelViewSet):
    queryset = SalaryStructure.objects.select_related('employee').all()
    serializer_class = SalaryStructureSerializer
    permission_classes = [IsAuthenticated, IsFinance]


class PayslipViewSet(viewsets.ModelViewSet):
    serializer_class = PayslipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Finance & HR Admins see all payslips
        if user.is_superuser or user.role in [UserRole.SUPER_ADMIN, UserRole.HR_ADMIN, UserRole.FINANCE]:
            return Payslip.objects.select_related('employee').all()

        # Regular Employees see ONLY their own payslips (IDOR Protection)
        if hasattr(user, 'employee_profile'):
            return Payslip.objects.select_related('employee').filter(employee=user.employee_profile)

        return Payslip.objects.none()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my(self, request):
        """GET /api/v1/payroll/payslips/my/"""
        employee = get_employee_by_user_id(request.user.id)
        if not employee:
            return Response({"success": False, "message": "No employee profile found."}, status=status.HTTP_404_NOT_FOUND)
        payslips = Payslip.objects.filter(employee=employee).order_by('-pay_period_year', '-pay_period_month')
        return Response({"success": True, "data": PayslipSerializer(payslips, many=True).data})
