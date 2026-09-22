import pytest
from django.urls import reverse
from rest_framework import status
from datetime import date
from accounts.models import UserRole
from accounts.services import create_user_account
from employees.services import create_employee_profile


@pytest.mark.django_db
class TestAIIntelligence:

    @pytest.fixture
    def setup_employee_with_skills(self):
        user = create_user_account(
            username='ai_emp', email='ai_emp@talentsphere.io', password='Password123!', role=UserRole.ENGINEER
        )
        emp = create_employee_profile(
            employee_id='EMP-999', first_name='John', last_name='Developer', email='ai_emp@talentsphere.io',
            joining_date=date(2025, 1, 1), user=user, skills=['Python', 'Django', 'SQL', 'React']
        )
        return user, emp

    def test_ai_skill_gap_analysis_execution(self, api_client, setup_employee_with_skills):
        user, emp = setup_employee_with_skills
        api_client.force_authenticate(user=user)

        url = reverse('ai_intelligence:skill_gap-analyze')
        payload = {
            'target_role': 'Full Stack Cloud Architect',
            'required_skills': ['Python', 'Django', 'FastAPI', 'PostgreSQL', 'Docker', 'AWS']
        }

        response = api_client.post(url, payload, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['success'] is True

        data = response.data['data']
        assert 'Python' in data['matched_skills']
        assert 'Django' in data['matched_skills']
        assert 'Docker' in data['missing_skills']
        assert 'AWS' in data['missing_skills']
        assert len(data['recommendations']) >= 2
