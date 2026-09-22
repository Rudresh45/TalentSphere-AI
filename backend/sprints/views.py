from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from sprints.models import Sprint
from sprints.serializers import SprintSerializer


class SprintViewSet(viewsets.ModelViewSet):
    queryset = Sprint.objects.select_related('project').prefetch_related('tasks').all()
    serializer_class = SprintSerializer
    permission_classes = [IsAuthenticated]
