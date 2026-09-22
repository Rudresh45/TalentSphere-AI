from django.db import models
from employees.models import Employee


class OffboardingStage(models.TextChoices):
    RESIGNATION_SUBMITTED = 'RESIGNATION_SUBMITTED', 'Resignation Submitted'
    MANAGER_APPROVAL = 'MANAGER_APPROVAL', 'Manager Approval'
    ASSET_RETURN = 'ASSET_RETURN', 'Asset Return'
    ACCESS_REVOCATION = 'ACCESS_REVOCATION', 'Access Revocation'
    FINAL_PAYROLL = 'FINAL_PAYROLL', 'Final Payroll Clearance'
    EXIT_INTERVIEW = 'EXIT_INTERVIEW', 'Exit Interview'
    DEACTIVATED = 'DEACTIVATED', 'Employee Deactivated'


class OffboardingWorkflow(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='offboarding_workflow')
    stage = models.CharField(
        max_length=30, choices=OffboardingStage.choices, default=OffboardingStage.RESIGNATION_SUBMITTED
    )
    resignation_date = models.DateField()
    last_working_day = models.DateField()
    assets_returned = models.BooleanField(default=False)
    access_revoked = models.BooleanField(default=False)
    exit_interview_completed = models.BooleanField(default=False)
    exit_interview_notes = models.TextField(blank=True, null=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Offboarding for {self.employee.full_name} [{self.get_stage_display()}]"
