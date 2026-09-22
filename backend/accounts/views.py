"""
TalentSphere Authentication & User Management API Views
"""
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from accounts.serializers import (
    CustomTokenObtainPairSerializer,
    UserSerializer,
    UserRegistrationSerializer,
    ChangePasswordSerializer,
    UserRoleUpdateSerializer
)
from accounts.permissions import IsSuperAdmin, IsHRAdmin
from accounts.services import create_user_account, update_user_password, update_user_role_service
from accounts.selectors import get_all_users, get_user_by_id


class LoginView(TokenObtainPairView):
    """
    POST /api/v1/auth/login/
    Obtain JWT Access & Refresh Token Pair.
    Throttled at 5 requests/minute to prevent brute-force attacks.
    """
    serializer_class = CustomTokenObtainPairSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'login'


class CustomTokenRefreshView(TokenRefreshView):
    """
    POST /api/v1/auth/refresh/
    Refresh expired JWT Access Token.
    """
    pass


class LogoutView(APIView):
    """
    POST /api/v1/auth/logout/
    Blacklist Refresh Token upon user logout.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {"success": False, "message": "Refresh token is required.", "error_code": "VALIDATION_ERROR"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"success": True, "message": "Successfully logged out."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"success": False, "message": str(e), "error_code": "INVALID_TOKEN"},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserRegisterView(generics.CreateAPIView):
    """
    POST /api/v1/auth/register/
    Register a new user account.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user_account(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            first_name=serializer.validated_data.get('first_name', ''),
            last_name=serializer.validated_data.get('last_name', ''),
            role=serializer.validated_data.get('role', 'EMPLOYEE'),
            phone=serializer.validated_data.get('phone')
        )
        return Response(
            {
                "success": True,
                "message": "User account registered successfully.",
                "data": UserSerializer(user).data
            },
            status=status.HTTP_201_CREATED
        )


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    GET /api/v1/auth/me/
    PATCH /api/v1/auth/me/
    Retrieve and update the authenticated user's profile.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_user_by_id(self.request.user.id)


class ChangePasswordView(APIView):
    """
    POST /api/v1/auth/change-password/
    Secure password update for authenticated users.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            update_user_password(
                user=request.user,
                old_password=serializer.validated_data['old_password'],
                new_password=serializer.validated_data['new_password']
            )
            return Response(
                {"success": True, "message": "Password updated successfully."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"success": False, "message": str(e), "error_code": "INVALID_PASSWORD"},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserListView(generics.ListAPIView):
    """
    GET /api/v1/auth/users/
    List all platform users. Restricted to HR Admin and Super Admin.
    """
    serializer_class = UserSerializer
    permission_classes = [IsHRAdmin]

    def get_queryset(self):
        return get_all_users()


class UserRoleUpdateView(APIView):
    """
    PATCH /api/v1/auth/users/<id>/role/
    Update user RBAC role. Strictly restricted to Super Admin.
    """
    permission_classes = [IsSuperAdmin]

    def patch(self, request, pk):
        target_user = get_user_by_id(pk)
        if not target_user:
            return Response(
                {"success": False, "message": "User not found.", "error_code": "NOT_FOUND"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserRoleUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            updated_user = update_user_role_service(
                target_user=target_user,
                new_role=serializer.validated_data['role'],
                updated_by=request.user
            )
            return Response(
                {
                    "success": True,
                    "message": f"Role updated to {updated_user.role} successfully.",
                    "data": UserSerializer(updated_user).data
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"success": False, "message": str(e), "error_code": "ROLE_UPDATE_FAILED"},
                status=status.HTTP_400_BAD_REQUEST
            )
