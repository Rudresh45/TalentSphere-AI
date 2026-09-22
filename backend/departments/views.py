from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from departments.models import Department, Designation
from departments.serializers import DepartmentSerializer, DesignationSerializer
from accounts.permissions import IsHRAdmin, IsManager


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Departments.
    Read: Authenticated users.
    Mutations: HR Admin & Super Admin.
    """
    queryset = Department.objects.prefetch_related('sub_departments', 'designations', 'employees').all()
    serializer_class = DepartmentSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsHRAdmin()]


class DesignationViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Designations.
    """
    queryset = Designation.objects.select_related('department').all()
    serializer_class = DesignationSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsHRAdmin()]
