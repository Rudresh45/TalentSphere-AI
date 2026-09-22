from django.db import models
from departments.models import Department
from employees.models import Employee


class ProjectStatus(models.TextChoices):
    PLANNING = 'PLANNING', 'Planning'
    ACTIVE = 'ACTIVE', 'Active'
    COMPLETED = 'COMPLETED', 'Completed'
    ON_HOLD = 'ON_HOLD', 'On Hold'


class Project(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects')
    owner = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='owned_projects')
    members = models.ManyToManyField(Employee, related_name='assigned_projects', blank=True)
    status = models.CharField(max_length=20, choices=ProjectStatus.choices, default=ProjectStatus.PLANNING)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.code})"
