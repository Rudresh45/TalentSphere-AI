from rest_framework import serializers
from offboarding.models import OffboardingWorkflow


class OffboardingWorkflowSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)

    class Meta:
        model = OffboardingWorkflow
        fields = (
            'id', 'employee', 'employee_name', 'stage', 'resignation_date',
            'last_working_day', 'assets_returned', 'access_revoked',
            'exit_interview_completed', 'exit_interview_notes', 'completed_at',
            'created_at', 'updated_at'
        )
