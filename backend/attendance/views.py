from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from attendance.models import AttendanceRecord
from attendance.serializers import AttendanceRecordSerializer, BreakRecordSerializer
from attendance.services import clock_in_employee, clock_out_employee, start_break, end_break
from employees.selectors import get_employee_by_user_id
from accounts.permissions import IsHRAdmin, IsManager
from accounts.models import UserRole


class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = AttendanceRecord.objects.select_related('employee', 'employee__user').prefetch_related('breaks').all()

        # Date filter
        date_param = self.request.query_params.get('date')
        if date_param:
            queryset = queryset.filter(date=date_param)

        # Super Admin & HR Admin see all
        if user.is_superuser or user.role in [UserRole.SUPER_ADMIN, UserRole.HR_ADMIN]:
            return queryset

        # Manager sees team attendance
        if user.role == UserRole.MANAGER and hasattr(user, 'employee_profile'):
            emp = user.employee_profile
            return queryset.filter(employee__manager=emp)

        # Employee sees own attendance
        if hasattr(user, 'employee_profile'):
            return queryset.filter(employee=user.employee_profile)

        return queryset.none()

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def clock_in(self, request):
        employee = get_employee_by_user_id(request.user.id)
        if not employee:
            return Response({"success": False, "message": "Employee profile required to clock in."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            record = clock_in_employee(employee=employee)
            return Response({"success": True, "message": "Clocked in successfully.", "data": AttendanceRecordSerializer(record).data})
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def clock_out(self, request):
        employee = get_employee_by_user_id(request.user.id)
        if not employee:
            return Response({"success": False, "message": "Employee profile required to clock out."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            record = clock_out_employee(employee=employee)
            return Response({"success": True, "message": "Clocked out successfully.", "data": AttendanceRecordSerializer(record).data})
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def start_break(self, request):
        employee = get_employee_by_user_id(request.user.id)
        if not employee:
            return Response({"success": False, "message": "Employee profile required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            b = start_break(employee=employee)
            return Response({"success": True, "message": "Break started.", "data": BreakRecordSerializer(b).data})
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def end_break(self, request):
        employee = get_employee_by_user_id(request.user.id)
        if not employee:
            return Response({"success": False, "message": "Employee profile required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            b = end_break(employee=employee)
            return Response({"success": True, "message": "Break ended.", "data": BreakRecordSerializer(b).data})
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my(self, request):
        employee = get_employee_by_user_id(request.user.id)
        if not employee:
            return Response({"success": False, "message": "No employee profile found."}, status=status.HTTP_404_NOT_FOUND)
        records = AttendanceRecord.objects.filter(employee=employee).order_by('-date')
        return Response({"success": True, "data": AttendanceRecordSerializer(records, many=True).data})

    @action(detail=False, methods=['get'], permission_classes=[IsManager])
    def team(self, request):
        employee = get_employee_by_user_id(request.user.id)
        if not employee:
            return Response({"success": False, "message": "No manager profile found."}, status=status.HTTP_404_NOT_FOUND)
        records = AttendanceRecord.objects.filter(employee__manager=employee).order_by('-date')
        return Response({"success": True, "data": AttendanceRecordSerializer(records, many=True).data})
