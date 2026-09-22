"""
TalentSphere RBAC & Object-Level Permissions Engine
"""
from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.models import UserRole


class IsSuperAdmin(BasePermission):
    """Allows access only to Super Admins."""
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and (
                request.user.role == UserRole.SUPER_ADMIN or request.user.is_superuser
            )
        )


class IsHRAdmin(BasePermission):
    """Allows access to HR Admins and Super Admins."""
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and (
                request.user.role in [UserRole.SUPER_ADMIN, UserRole.HR_ADMIN] or request.user.is_superuser
            )
        )


class IsHRManager(BasePermission):
    """Allows access to HR Managers, HR Admins, and Super Admins."""
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and (
                request.user.role in [UserRole.SUPER_ADMIN, UserRole.HR_ADMIN, UserRole.HR_MANAGER] or request.user.is_superuser
            )
        )


class IsManager(BasePermission):
    """Allows access to Managers, HR Managers/Admins, and Super Admins."""
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and (
                request.user.role in [UserRole.SUPER_ADMIN, UserRole.HR_ADMIN, UserRole.HR_MANAGER, UserRole.MANAGER] or request.user.is_superuser
            )
        )


class IsEngineer(BasePermission):
    """Allows access to Engineers, Managers, and Admins."""
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and (
                request.user.role in [UserRole.SUPER_ADMIN, UserRole.ENGINEER, UserRole.MANAGER] or request.user.is_superuser
            )
        )


class IsRecruiter(BasePermission):
    """Allows access to Recruiters, HR Admins, and Super Admins."""
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and (
                request.user.role in [UserRole.SUPER_ADMIN, UserRole.HR_ADMIN, UserRole.HR_MANAGER, UserRole.RECRUITER] or request.user.is_superuser
            )
        )


class IsFinance(BasePermission):
    """Allows access to Finance personnel, HR Admins, and Super Admins."""
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and (
                request.user.role in [UserRole.SUPER_ADMIN, UserRole.HR_ADMIN, UserRole.FINANCE] or request.user.is_superuser
            )
        )


class IsEmployee(BasePermission):
    """Allows access to any authenticated employee."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsOwnerOrManagerOrHR(BasePermission):
    """
    Object-Level Authorization:
    Checks if the requesting user is the object owner, their direct manager, or HR/Super Admin.
    Protects against IDOR attacks.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Super Admin and HR Admin always have full access
        if user.is_superuser or user.role in [UserRole.SUPER_ADMIN, UserRole.HR_ADMIN]:
            return True

        # Extract target user from object
        target_user = None
        if hasattr(obj, 'user'):
            target_user = obj.user
        elif isinstance(obj, type(user)):
            target_user = obj

        if target_user and target_user == user:
            return True

        # Check if requesting user is manager of the employee target
        if hasattr(obj, 'manager') and obj.manager:
            if hasattr(user, 'employee_profile') and obj.manager == user.employee_profile:
                return True
            if obj.manager.user == user:
                return True

        # Read-only permission for HR Managers within department if applicable
        if user.role == UserRole.HR_MANAGER and request.method in SAFE_METHODS:
            return True

        return False
