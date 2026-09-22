from django.db import models
from employees.models import Employee


class OnboardingStage(models.TextChoices):
    OFFER_ACCEPTED = 'OFFER_ACCEPTED', 'Offer Accepted'
    DOCUMENT_COLLECTION = 'DOCUMENT_COLLECTION', 'Document Collection'
    ACCOUNT_CREATION = 'ACCOUNT_CREATION', 'Account Creation'
    DEPARTMENT_ASSIGNMENT = 'DEPARTMENT_ASSIGNMENT', 'Department Assignment'
    EQUIPMENT_ASSIGNMENT = 'EQUIPMENT_ASSIGNMENT', 'Equipment Assignment'
    TRAINING = 'TRAINING', 'Training & Orientation'
    COMPLETED = 'COMPLETED', 'Onboarding Completed'


class OnboardingWorkflow(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='onboarding_workflow')
    stage = models.CharField(
        max_length=30, choices=OnboardingStage.choices, default=OnboardingStage.OFFER_ACCEPTED
    )
    documents_submitted = models.BooleanField(default=False)
    equipment_assigned = models.BooleanField(default=False)
    training_completed = models.BooleanField(default=False)
    target_completion_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Onboarding for {self.employee.full_name} [{self.get_stage_display()}]"
