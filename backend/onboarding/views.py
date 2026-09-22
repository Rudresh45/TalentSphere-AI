from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from onboarding.models import OnboardingWorkflow
from onboarding.serializers import OnboardingWorkflowSerializer
from accounts.permissions import IsHRAdmin


class OnboardingViewSet(viewsets.ModelViewSet):
    queryset = OnboardingWorkflow.objects.select_related('employee').all()
    serializer_class = OnboardingWorkflowSerializer
    permission_classes = [IsAuthenticated, IsHRAdmin]
