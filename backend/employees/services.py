"""
TalentSphere Employee Management Business Services
"""
from django.db import transaction
from django.core.exceptions import ValidationError
from employees.models import Employee, EmployeeStatus, EmploymentType
from accounts.models import User, UserRole
from accounts.services import create_user_account


def create_employee_profile(
    *,
    employee_id: str,
    first_name: str,
    last_name: str,
    email: str,
    phone: str = None,
    department_id: int = None,
    designation_id: int = None,
    manager_id: int = None,
    joining_date,
    employment_type: str = EmploymentType.FULL_TIME,
    skills: list = None,
    experience_years: float = 0.0,
    salary: float = 0.00,
    user: User = None,
    role: str = UserRole.EMPLOYEE
) -> Employee:
    """
    Service to onboard an employee.
    If User is not provided, automatically provisions a User account.
    """
    if Employee.objects.filter(employee_id__iexact=employee_id).exists():
        raise ValidationError(f"Employee ID '{employee_id}' already exists.")

    with transaction.atomic():
        if not user:
            # Auto-create user credentials
            username = email.split('@')[0].lower()
            temp_password = f"Talent_{employee_id}!"
            user = create_user_account(
                username=username,
                email=email,
                password=temp_password,
                first_name=first_name,
                last_name=last_name,
                role=role,
                phone=phone
            )

        employee = Employee.objects.create(
            employee_id=employee_id,
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=email.lower(),
            phone=phone,
            department_id=department_id,
            designation_id=designation_id,
            manager_id=manager_id,
            joining_date=joining_date,
            employment_type=employment_type,
            skills=skills or [],
            experience_years=experience_years,
            salary=salary,
            status=EmployeeStatus.ACTIVE
        )
        return employee


def update_employee_profile(*, employee: Employee, data: dict) -> Employee:
    """
    Service to update an employee profile with validation.
    """
    for key, value in data.items():
        if hasattr(employee, key):
            setattr(employee, key, value)
    
    employee.save()
    return employee


def change_employee_status(*, employee: Employee, new_status: str) -> Employee:
    """
    Service to transition employee status (ACTIVE, ON_LEAVE, TERMINATED).
    If terminated, deactivates linked user account.
    """
    if new_status not in EmployeeStatus.values:
        raise ValidationError(f"Invalid status '{new_status}'.")

    with transaction.atomic():
        employee.status = new_status
        employee.save()

        if new_status == EmployeeStatus.TERMINATED:
            employee.user.is_active = False
            employee.user.save()

        return employee
