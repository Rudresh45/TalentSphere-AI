"""
TalentSphere Account & Identity Business Services Layer
"""
from django.db import transaction
from django.core.exceptions import ValidationError
from accounts.models import User, Profile, UserRole


def create_user_account(*, username: str, email: str, password: str, first_name: str = "", last_name: str = "", role: str = UserRole.EMPLOYEE, phone: str = None) -> User:
    """
    Service to create a new User account along with their default Profile.
    Enforces atomic transaction and validation.
    """
    if User.objects.filter(username__iexact=username).exists():
        raise ValidationError("Username already taken.")
    if User.objects.filter(email__iexact=email).exists():
        raise ValidationError("Email address already registered.")

    with transaction.atomic():
        user = User.objects.create_user(
            username=username,
            email=email.lower(),
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=role,
            phone=phone
        )
        Profile.objects.create(user=user)
        return user


def update_user_password(*, user: User, old_password: str, new_password: str) -> None:
    """
    Service to update a user's password securely.
    """
    if not user.check_password(old_password):
        raise ValidationError("Invalid current password.")
    
    user.set_password(new_password)
    user.save()


def update_user_role_service(*, target_user: User, new_role: str, updated_by: User) -> User:
    """
    Service to change a user's RBAC role. Only Super Admin can change roles.
    """
    if not updated_by.is_super_admin:
        raise ValidationError("Only Super Admins can alter user roles.")
    
    if new_role not in UserRole.values:
        raise ValidationError(f"Invalid role '{new_role}'.")

    target_user.role = new_role
    target_user.save()
    return target_user
