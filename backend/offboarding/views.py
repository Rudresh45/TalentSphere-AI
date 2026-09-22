from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from offboarding.models import OffboardingWorkflow
from offboarding.serializers import OffboardingWorkflowSerializer
from accounts.permissions import IsHRAdmin


class OffboardingViewSet(viewsets.ModelViewSet):
    queryset = OffboardingWorkflow.objects.select_related('employee').all()
    serializer_class = OffboardingWorkflowSerializer
    permission_classes = [IsAuthenticated, IsHRAdmin]
