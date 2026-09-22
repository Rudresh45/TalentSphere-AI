import pytest
from django.urls import reverse
from rest_framework import status
from datetime import date
from accounts.models import UserRole
from accounts.services import create_user_account
from employees.services import create_employee_profile
from departments.models import Department, Designation


@pytest.mark.django_db
class TestIDORSecurity:

    @pytest.fixture
    def setup_employees(self):
        dept = Department.objects.create(name='Engineering', code='ENG')
        desig = Designation.objects.create(title='Software Engineer', code='SE', department=dept)

        # Create Manager
        mgr_user = create_user_account(
            username='mgr1', email='mgr1@talentsphere.io', password='Password123!', role=UserRole.MANAGER
        )
        mgr_emp = create_employee_profile(
            employee_id='EMP-100', first_name='Manager', last_name='One', email='mgr1@talentsphere.io',
            joining_date=date(2025, 1, 1), user=mgr_user, department_id=dept.id, designation_id=desig.id
        )

        # Create Employee 1 (Managed by Manager One)
        emp1_user = create_user_account(
            username='emp1', email='emp1@talentsphere.io', password='Password123!', role=UserRole.EMPLOYEE
        )
        emp1 = create_employee_profile(
            employee_id='EMP-101', first_name='Alice', last_name='Smith', email='emp1@talentsphere.io',
            joining_date=date(2025, 2, 1), user=emp1_user, manager_id=mgr_emp.id, department_id=dept.id
        )

        # Create Employee 2 (Unrelated Employee)
        emp2_user = create_user_account(
            username='emp2', email='emp2@talentsphere.io', password='Password123!', role=UserRole.EMPLOYEE
        )
        emp2 = create_employee_profile(
            employee_id='EMP-102', first_name='Bob', last_name='Jones', email='emp2@talentsphere.io',
            joining_date=date(2025, 3, 1), user=emp2_user, department_id=dept.id
        )

        return {
            'manager': mgr_user,
            'manager_emp': mgr_emp,
            'emp1_user': emp1_user,
            'emp1': emp1,
            'emp2_user': emp2_user,
            'emp2': emp2
        }

    def test_employee_cannot_access_another_employee_profile_idor(self, api_client, setup_employees):
        data = setup_employees
        # Employee 1 tries accessing Employee 2 profile: GET /api/v1/employees/{emp2.id}/
        api_client.force_authenticate(user=data['emp1_user'])
        url = reverse('employees:employee-detail', kwargs={'pk': data['emp2'].id})
        response = api_client.get(url)

        # Must return 403 Forbidden or 404 Not Found to prevent IDOR vulnerability
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]

    def test_employee_can_access_own_profile(self, api_client, setup_employees):
        data = setup_employees
        api_client.force_authenticate(user=data['emp1_user'])
        url = reverse('employees:employee-detail', kwargs={'pk': data['emp1'].id})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == 'Alice'

    def test_manager_can_access_team_member_profile(self, api_client, setup_employees):
        data = setup_employees
        api_client.force_authenticate(user=data['manager'])
        url = reverse('employees:employee-detail', kwargs={'pk': data['emp1'].id})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == 'Alice'
