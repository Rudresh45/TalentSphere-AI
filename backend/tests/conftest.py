import pytest
from rest_framework.test import APIClient
from accounts.models import User, UserRole, Profile
from accounts.services import create_user_account


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def super_admin_user(db):
    return create_user_account(
        username='superadmin',
        email='superadmin@talentsphere.io',
        password='Password123!',
        first_name='Super',
        last_name='Admin',
        role=UserRole.SUPER_ADMIN
    )


@pytest.fixture
def hr_admin_user(db):
    return create_user_account(
        username='hradmin',
        email='hradmin@talentsphere.io',
        password='Password123!',
        first_name='HR',
        last_name='Admin',
        role=UserRole.HR_ADMIN
    )


@pytest.fixture
def manager_user(db):
    return create_user_account(
        username='manager',
        email='manager@talentsphere.io',
        password='Password123!',
        first_name='Team',
        last_name='Manager',
        role=UserRole.MANAGER
    )


@pytest.fixture
def engineer_user(db):
    return create_user_account(
        username='engineer',
        email='engineer@talentsphere.io',
        password='Password123!',
        first_name='Lead',
        last_name='Engineer',
        role=UserRole.ENGINEER
    )


@pytest.fixture
def employee_user(db):
    return create_user_account(
        username='employee',
        email='employee@talentsphere.io',
        password='Password123!',
        first_name='John',
        last_name='Doe',
        role=UserRole.EMPLOYEE
    )


@pytest.fixture
def finance_user(db):
    return create_user_account(
        username='finance',
        email='finance@talentsphere.io',
        password='Password123!',
        first_name='Fin',
        last_name='Officer',
        role=UserRole.FINANCE
    )
