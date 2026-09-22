from django.db import models
from departments.models import Department
from employees.models import Employee


class JobStatus(models.TextChoices):
    OPEN = 'OPEN', 'Open'
    CLOSED = 'CLOSED', 'Closed'
    ON_HOLD = 'ON_HOLD', 'On Hold'


class ApplicationStatus(models.TextChoices):
    APPLIED = 'APPLIED', 'Applied'
    SCREENING = 'SCREENING', 'Screening'
    SHORTLISTED = 'SHORTLISTED', 'Shortlisted'
    INTERVIEW = 'INTERVIEW', 'Interview Scheduled'
    TECHNICAL_ROUND = 'TECHNICAL_ROUND', 'Technical Round'
    HR_ROUND = 'HR_ROUND', 'HR Round'
    SELECTED = 'SELECTED', 'Selected'
    REJECTED = 'REJECTED', 'Rejected'


class InterviewRecommendation(models.TextChoices):
    HIRE = 'HIRE', 'Strong Hire'
    LEAN_HIRE = 'LEAN_HIRE', 'Lean Hire'
    NEUTRAL = 'NEUTRAL', 'Neutral'
    REJECT = 'REJECT', 'Reject'


class JobPosition(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='job_positions')
    description = models.TextField()
    required_skills = models.JSONField(default=list, help_text="List of required skills")
    min_experience = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)
    salary_range = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, choices=JobStatus.choices, default=JobStatus.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.code})"


class Candidate(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    resume_url = models.URLField(blank=True, null=True)
    skills = models.JSONField(default=list, blank=True)
    experience_years = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class Application(models.Model):
    job = models.ForeignKey(JobPosition, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=30, choices=ApplicationStatus.choices, default=ApplicationStatus.APPLIED)
    notes = models.TextField(blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.candidate} - {self.job.title} [{self.get_status_display()}]"


class InterviewSchedule(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='interviews')
    interviewer = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='interviews_to_conduct')
    scheduled_time = models.DateTimeField()
    meeting_link = models.URLField(blank=True, null=True)
    round_name = models.CharField(max_length=50, default="Technical Round")
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interview for {self.application.candidate} with {self.interviewer}"


class InterviewFeedback(models.Model):
    interview = models.OneToOneField(InterviewSchedule, on_delete=models.CASCADE, related_name='feedback')
    score = models.IntegerField(help_text="Score 1 to 10")
    comments = models.TextField()
    recommendation = models.CharField(max_length=20, choices=InterviewRecommendation.choices, default=InterviewRecommendation.NEUTRAL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback ({self.score}/10) for {self.interview}"
