"""
TalentSphere Employee API Views & RBAC Authorization Pipeline
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from employees.models import Employee, EmployeeStatus
from employees.serializers import EmployeeSerializer, EmployeeListSerializer
from employees.selectors import get_all_employees, get_employee_by_id, get_employee_by_user_id
from employees.services import create_employee_profile, update_employee_profile, change_employee_status
from accounts.permissions import IsHRAdmin, IsManager, IsOwnerOrManagerOrHR
from accounts.models import UserRole


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    Employee Management API:
    - Listing: HR Admins see all; Managers see team members; Employees see own record.
    - Detail: Enforces object-level permission check (IsOwnerOrManagerOrHR) to prevent IDOR attacks.
    - Mutations: Restricted to HR Admin / Super Admin.
    """
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrManagerOrHR]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'email', 'employee_id', 'skills']
    ordering_fields = ['joining_date', 'first_name', 'last_name', 'salary']
    ordering = ['-joining_date']

    def get_queryset(self):
        user = self.request.user
        queryset = get_all_employees()

        # Department filtering via query param
        department_id = self.request.query_params.get('department')
        if department_id:
            queryset = queryset.filter(department_id=department_id)

        # Status filtering via query param
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)

        # Super Admin & HR Admin see all employees
        if user.is_superuser or user.role in [UserRole.SUPER_ADMIN, UserRole.HR_ADMIN]:
            return queryset

        # HR Manager sees employees in their department
        if user.role == UserRole.HR_MANAGER and hasattr(user, 'employee_profile'):
            emp = user.employee_profile
            if emp and emp.department:
                return queryset.filter(department=emp.department)

        # Manager sees their team members + self
        if user.role == UserRole.MANAGER and hasattr(user, 'employee_profile'):
            emp = user.employee_profile
            if emp:
                return queryset.filter(models.Q(manager=emp) | models.Q(id=emp.id))

        # Regular Employees see only their own profile
        if hasattr(user, 'employee_profile'):
            return queryset.filter(id=user.employee_profile.id)

        return queryset.none()

    def get_serializer_class(self):
        if self.action == 'list':
            return EmployeeListSerializer
        return EmployeeSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsHRAdmin()]
        return [IsAuthenticated(), IsOwnerOrManagerOrHR()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        employee = create_employee_profile(
            employee_id=serializer.validated_data['employee_id'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],
            email=serializer.validated_data['email'],
            phone=serializer.validated_data.get('phone'),
            department_id=serializer.validated_data.get('department').id if serializer.validated_data.get('department') else None,
            designation_id=serializer.validated_data.get('designation').id if serializer.validated_data.get('designation') else None,
            manager_id=serializer.validated_data.get('manager').id if serializer.validated_data.get('manager') else None,
            joining_date=serializer.validated_data['joining_date'],
            employment_type=serializer.validated_data.get('employment_type', 'FULL_TIME'),
            skills=serializer.validated_data.get('skills', []),
            experience_years=serializer.validated_data.get('experience_years', 0.0),
            salary=serializer.validated_data.get('salary', 0.00)
        )
        return Response(
            {
                "success": True,
                "message": "Employee created successfully.",
                "data": EmployeeSerializer(employee).data
            },
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        GET /api/v1/employees/me/
        Shortcut endpoint to retrieve logged-in employee profile.
        """
        employee = get_employee_by_user_id(request.user.id)
        if not employee:
            return Response(
                {"success": False, "message": "No employee profile found for this user.", "error_code": "NOT_FOUND"},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {"success": True, "data": EmployeeSerializer(employee).data},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['patch'], permission_classes=[IsHRAdmin])
    def update_status(self, request, pk=None):
        """
        PATCH /api/v1/employees/{id}/update_status/
        Update employee employment status (ACTIVE, ON_LEAVE, TERMINATED).
        """
        employee = self.get_object()
        new_status = request.data.get('status')
        if not new_status:
            return Response(
                {"success": False, "message": "Status is required.", "error_code": "VALIDATION_ERROR"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            updated_emp = change_employee_status(employee=employee, new_status=new_status)
            return Response(
                {
                    "success": True,
                    "message": f"Employee status updated to {new_status}.",
                    "data": EmployeeSerializer(updated_emp).data
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"success": False, "message": str(e), "error_code": "STATUS_UPDATE_FAILED"},
                status=status.HTTP_400_BAD_REQUEST
            )
