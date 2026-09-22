import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestThrottling:

    def test_login_throttling_exceeded(self, api_client, employee_user):
        url = reverse('accounts:login')
        # Login rate is configured to 5/minute
        for _ in range(5):
            api_client.post(url, {'username': 'employee', 'password': 'WrongPassword'})

        # 6th attempt should be throttled with HTTP 429
        response = api_client.post(url, {'username': 'employee', 'password': 'WrongPassword'})
        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        assert response.data['error_code'] == 'TOO_MANY_REQUESTS'
