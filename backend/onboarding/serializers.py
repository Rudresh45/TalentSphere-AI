from rest_framework import serializers
from onboarding.models import OnboardingWorkflow


class OnboardingWorkflowSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)

    class Meta:
        model = OnboardingWorkflow
        fields = (
            'id', 'employee', 'employee_name', 'stage', 'documents_submitted',
            'equipment_assigned', 'training_completed', 'target_completion_date',
            'completed_at', 'notes', 'created_at', 'updated_at'
        )
