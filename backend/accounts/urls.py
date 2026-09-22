from django.urls import path
from accounts.views import (
    LoginView,
    CustomTokenRefreshView,
    LogoutView,
    UserRegisterView,
    UserProfileView,
    ChangePasswordView,
    UserListView,
    UserRoleUpdateView
)

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('me/', UserProfileView.as_view(), name='user_profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/role/', UserRoleUpdateView.as_view(), name='user_role_update'),
]
