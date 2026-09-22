from rest_framework import serializers
from departments.models import Department, Designation


class DesignationSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Designation
        fields = ('id', 'title', 'code', 'department', 'department_name', 'grade', 'created_at')


class DepartmentSerializer(serializers.ModelSerializer):
    sub_departments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    designations = DesignationSerializer(many=True, read_only=True)
    employee_count = serializers.IntegerField(source='employees.count', read_only=True)

    class Meta:
        model = Department
        fields = (
            'id', 'name', 'code', 'description', 'parent_department',
            'sub_departments', 'designations', 'employee_count', 'created_at', 'updated_at'
        )
