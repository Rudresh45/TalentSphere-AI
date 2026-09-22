from django.db import models
from projects.models import Project
from tasks.models import Task


class SprintStatus(models.TextChoices):
    PLANNING = 'PLANNING', 'Planning'
    ACTIVE = 'ACTIVE', 'Active'
    REVIEW = 'REVIEW', 'In Review'
    COMPLETED = 'COMPLETED', 'Completed'


class Sprint(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='sprints')
    name = models.CharField(max_length=100)
    goal = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=SprintStatus.choices, default=SprintStatus.PLANNING)
    tasks = models.ManyToManyField(Task, related_name='sprints', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.project.code} - {self.name} [{self.get_status_display()}]"
