from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from projects.models import Project
from projects.serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.select_related('department', 'owner').prefetch_related('members').all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
