from django.db import models
from employees.models import Employee


class PerformanceReview(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='performance_reviews')
    reviewer = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='conducted_reviews')
    review_period = models.CharField(max_length=50, help_text="e.g. Q1 2026 or Annual 2025")
    score = models.DecimalField(max_digits=3, decimal_places=1, help_text="Rating out of 5.0")
    strengths = models.TextField(blank=True, null=True)
    areas_for_improvement = models.TextField(blank=True, null=True)
    goals = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Performance Review ({self.review_period}) for {self.employee.full_name}"
