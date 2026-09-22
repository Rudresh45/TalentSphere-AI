from rest_framework import serializers
from employees.models import Employee, EmploymentType, EmployeeStatus
from departments.serializers import DepartmentSerializer, DesignationSerializer
from accounts.serializers import UserSerializer


class EmployeeSerializer(serializers.ModelSerializer):
    department_detail = DepartmentSerializer(source='department', read_only=True)
    designation_detail = DesignationSerializer(source='designation', read_only=True)
    user_detail = UserSerializer(source='user', read_only=True)
    manager_name = serializers.CharField(source='manager.full_name', read_only=True)

    class Meta:
        model = Employee
        fields = (
            'id', 'employee_id', 'user', 'user_detail', 'first_name', 'last_name',
            'full_name', 'email', 'phone', 'department', 'department_detail',
            'designation', 'designation_detail', 'manager', 'manager_name',
            'joining_date', 'employment_type', 'skills', 'experience_years',
            'salary', 'status', 'created_at', 'updated_at'
        )
        read_only_fields = ('created_at', 'updated_at')

    def validate_salary(self, value):
        if value < 0:
            raise serializers.ValidationError("Salary cannot be negative.")
        return value

    def validate_email(self, value):
        user_obj = self.context.get('request').user if self.context.get('request') else None
        existing = Employee.objects.filter(email__iexact=value)
        if self.instance:
            existing = existing.exclude(id=self.instance.id)
        if existing.exists():
            raise serializers.ValidationError("An employee with this email already exists.")
        return value.lower()


class EmployeeListSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    designation_title = serializers.CharField(source='designation.title', read_only=True)

    class Meta:
        model = Employee
        fields = (
            'id', 'employee_id', 'first_name', 'last_name', 'full_name',
            'email', 'department_name', 'designation_title', 'employment_type', 'status'
        )
