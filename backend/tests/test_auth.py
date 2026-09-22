import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestAuthentication:

    def test_login_success(self, api_client, employee_user):
        url = reverse('accounts:login')
        response = api_client.post(url, {
            'username': 'employee',
            'password': 'Password123!'
        })
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert response.data['user']['role'] == 'EMPLOYEE'

    def test_login_invalid_password(self, api_client, employee_user):
        url = reverse('accounts:login')
        response = api_client.post(url, {
            'username': 'employee',
            'password': 'WrongPassword!'
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['error_code'] == 'UNAUTHORIZED'

    def test_token_refresh(self, api_client, employee_user):
        login_url = reverse('accounts:login')
        login_res = api_client.post(login_url, {
            'username': 'employee',
            'password': 'Password123!'
        })
        refresh_token = login_res.data['refresh']

        refresh_url = reverse('accounts:token_refresh')
        response = api_client.post(refresh_url, {'refresh': refresh_token})
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data

    def test_logout_blacklists_token(self, api_client, employee_user):
        login_url = reverse('accounts:login')
        login_res = api_client.post(login_url, {
            'username': 'employee',
            'password': 'Password123!'
        })
        access_token = login_res.data['access']
        refresh_token = login_res.data['refresh']

        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        logout_url = reverse('accounts:logout')
        response = api_client.post(logout_url, {'refresh': refresh_token})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] is True

        # Ensure refresh token is blacklisted
        refresh_url = reverse('accounts:token_refresh')
        fail_res = api_client.post(refresh_url, {'refresh': refresh_token})
        assert fail_res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_current_user_profile(self, api_client, employee_user):
        login_url = reverse('accounts:login')
        login_res = api_client.post(login_url, {
            'username': 'employee',
            'password': 'Password123!'
        })
        access_token = login_res.data['access']

        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        me_url = reverse('accounts:user_profile')
        response = api_client.get(me_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == 'employee'
        assert response.data['role'] == 'EMPLOYEE'
