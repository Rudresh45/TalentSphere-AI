"""
TalentSphere Employee Selector & Query Optimization Layer
Prevents N+1 database query bugs using select_related.
"""
from django.db.models import QuerySet
from employees.models import Employee


def get_all_employees() -> QuerySet[Employee]:
    """Retrieve all employees with optimized joins for department, designation, and user."""
    return Employee.objects.select_related(
        'user', 'department', 'designation', 'manager', 'manager__user'
    ).all()


def get_employee_by_id(employee_id: int) -> Employee | None:
    """Retrieve a single employee record by PK."""
    try:
        return Employee.objects.select_related(
            'user', 'department', 'designation', 'manager', 'user__profile'
        ).get(id=employee_id)
    except Employee.DoesNotExist:
        return None


def get_employee_by_user_id(user_id: int) -> Employee | None:
    """Retrieve employee record linked to a User instance."""
    try:
        return Employee.objects.select_related(
            'user', 'department', 'designation', 'manager'
        ).get(user_id=user_id)
    except Employee.DoesNotExist:
        return None


def get_team_members_for_manager(manager_employee_id: int) -> QuerySet[Employee]:
    """Retrieve all employees managed by a specific manager."""
    return Employee.objects.select_related(
        'user', 'department', 'designation'
    ).filter(manager_id=manager_employee_id)
