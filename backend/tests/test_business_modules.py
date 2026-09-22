import pytest
from django.urls import reverse
from rest_framework import status
from datetime import date
from accounts.models import UserRole
from accounts.services import create_user_account
from employees.services import create_employee_profile
from departments.models import Department
from projects.models import Project
from tasks.models import Task, TaskStatus
from payroll.models import Payslip


@pytest.mark.django_db
class TestBusinessModules:

    @pytest.fixture
    def setup_data(self):
        dept = Department.objects.create(name='Operations', code='OPS')
        
        # User & Employee
        emp_user = create_user_account(
            username='ops_emp', email='ops_emp@talentsphere.io', password='Password123!', role=UserRole.EMPLOYEE
        )
        emp = create_employee_profile(
            employee_id='EMP-700', first_name='Sam', last_name='Ops', email='ops_emp@talentsphere.io',
            joining_date=date(2025, 1, 1), user=emp_user, department_id=dept.id
        )

        # Finance User
        fin_user = create_user_account(
            username='fin_user', email='fin@talentsphere.io', password='Password123!', role=UserRole.FINANCE
        )

        return emp_user, emp, fin_user

    def test_attendance_clock_in_clock_out_flow(self, api_client, setup_data):
        emp_user, emp, _ = setup_data
        api_client.force_authenticate(user=emp_user)

        # Clock In
        clock_in_url = reverse('attendance:attendance-clock-in')
        res_in = api_client.post(clock_in_url)
        assert res_in.status_code == status.HTTP_200_OK
        assert res_in.data['success'] is True

        # Clock Out
        clock_out_url = reverse('attendance:attendance-clock-out')
        res_out = api_client.post(clock_out_url)
        assert res_out.status_code == status.HTTP_200_OK
        assert res_out.data['success'] is True
        assert float(res_out.data['data']['total_hours']) >= 0.0

    def test_payroll_payslip_isolation(self, api_client, setup_data):
        emp_user, emp, fin_user = setup_data

        # Create Payslip
        Payslip.objects.create(
            employee=emp, pay_period_month=3, pay_period_year=2026,
            basic=5000.00, allowances=1000.00, deductions=500.00, net_salary=5500.00
        )

        # Employee retrieves own payslip
        api_client.force_authenticate(user=emp_user)
        my_url = reverse('payroll:payslip-my')
        res = api_client.get(my_url)
        assert res.status_code == status.HTTP_200_OK
        assert len(res.data['data']) == 1
        assert res.data['data'][0]['net_salary'] == '5500.00'

    def test_projects_and_kanban_tasks(self, api_client, setup_data):
        emp_user, emp, _ = setup_data
        api_client.force_authenticate(user=emp_user)

        # Create Project
        proj = Project.objects.create(name='Mobile App', code='MOB-01', owner=emp)
        
        # Create Task
        task = Task.objects.create(project=proj, title='Fix Auth Bug', assignee=emp, status=TaskStatus.TODO)

        url = reverse('tasks:task-list')
        res = api_client.get(url)
        assert res.status_code == status.HTTP_200_OK
        assert res.data['results'][0]['title'] == 'Fix Auth Bug'
