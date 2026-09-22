"""
TalentSphere Account & Identity Selector / Query Layer
"""
from django.db.models import QuerySet
from accounts.models import User


def get_all_users() -> QuerySet[User]:
    """Retrieve all users with select_related profile to prevent N+1 queries."""
    return User.objects.select_related('profile').all()


def get_user_by_id(user_id: int) -> User | None:
    """Retrieve a single user with profile optimization."""
    try:
        return User.objects.select_related('profile').get(id=user_id)
    except User.DoesNotExist:
        return None


def get_users_by_role(role: str) -> QuerySet[User]:
    """Filter users by enterprise role."""
    return User.objects.select_related('profile').filter(role=role)
