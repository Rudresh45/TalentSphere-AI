from django.contrib.auth.models import AbstractUser
from django.db import models

class UserRole(models.TextChoices):
    SUPER_ADMIN = 'SUPER_ADMIN', 'Super Admin'
    HR_ADMIN = 'HR_ADMIN', 'HR Admin'
    HR_MANAGER = 'HR_MANAGER', 'HR Manager'
    MANAGER = 'MANAGER', 'Manager'
    ENGINEER = 'ENGINEER', 'Engineer'
    EMPLOYEE = 'EMPLOYEE', 'Employee'
    RECRUITER = 'RECRUITER', 'Recruiter'
    FINANCE = 'FINANCE', 'Finance'


class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.EMPLOYEE,
        db_index=True,
        help_text="Role-Based Access Control Role"
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    skills = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
