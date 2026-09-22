from django.db import models
from employees.models import Employee


class PriorityLevel(models.TextChoices):
    HIGH = 'HIGH', 'High Priority'
    MEDIUM = 'MEDIUM', 'Medium Priority'
    LOW = 'LOW', 'Low Priority'


class SkillGapAnalysis(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='skill_gap_analyses')
    target_role = models.CharField(max_length=100)
    match_percentage = models.FloatField(help_text="Skill match percentage e.g. 65.5")
    matched_skills = models.JSONField(default=list)
    missing_skills = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Skill Gap Analysis ({self.target_role}) for {self.employee.full_name} - {self.match_percentage}%"


class LearningRecommendation(models.Model):
    analysis = models.ForeignKey(SkillGapAnalysis, on_delete=models.CASCADE, related_name='recommendations')
    skill_gap = models.CharField(max_length=100)
    course_title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=20, choices=PriorityLevel.choices, default=PriorityLevel.HIGH)
    recommended_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.priority}] {self.course_title} for {self.skill_gap}"
