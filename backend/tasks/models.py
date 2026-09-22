from django.db import models
from projects.models import Project
from employees.models import Employee


class TaskStatus(models.TextChoices):
    TODO = 'TODO', 'To Do'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    REVIEW = 'REVIEW', 'In Review'
    BLOCKED = 'BLOCKED', 'Blocked'
    COMPLETED = 'COMPLETED', 'Completed'


class TaskPriority(models.TextChoices):
    LOW = 'LOW', 'Low'
    MEDIUM = 'MEDIUM', 'Medium'
    HIGH = 'HIGH', 'High'
    URGENT = 'URGENT', 'Urgent'


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    assignee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    reporter = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='reported_tasks')
    status = models.CharField(max_length=20, choices=TaskStatus.choices, default=TaskStatus.TODO, db_index=True)
    priority = models.CharField(max_length=20, choices=TaskPriority.choices, default=TaskPriority.MEDIUM)
    estimated_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    logged_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['project', 'status']),
            models.Index(fields=['assignee']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"[{self.project.code}] {self.title} ({self.get_status_display()})"
