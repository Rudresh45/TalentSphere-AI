import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestPermissions:

    def test_user_list_allowed_for_hr_admin(self, api_client, hr_admin_user):
        api_client.force_authenticate(user=hr_admin_user)
        url = reverse('accounts:user_list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_user_list_denied_for_regular_employee(self, api_client, employee_user):
        api_client.force_authenticate(user=employee_user)
        url = reverse('accounts:user_list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data['error_code'] == 'PERMISSION_DENIED'

    def test_role_update_allowed_for_super_admin(self, api_client, super_admin_user, employee_user):
        api_client.force_authenticate(user=super_admin_user)
        url = reverse('accounts:user_role_update', kwargs={'pk': employee_user.id})
        response = api_client.patch(url, {'role': 'MANAGER'})
        assert response.status_code == status.HTTP_200_OK
        employee_user.refresh_from_db()
        assert employee_user.role == 'MANAGER'

    def test_role_update_denied_for_hr_admin(self, api_client, hr_admin_user, employee_user):
        api_client.force_authenticate(user=hr_admin_user)
        url = reverse('accounts:user_role_update', kwargs={'pk': employee_user.id})
        response = api_client.patch(url, {'role': 'MANAGER'})
        assert response.status_code == status.HTTP_403_FORBIDDEN
