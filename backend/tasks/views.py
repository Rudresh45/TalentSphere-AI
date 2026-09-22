from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from tasks.models import Task
from tasks.serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related('project', 'assignee', 'reporter').all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'project__code']
    ordering_fields = ['due_date', 'priority', 'status', 'created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        project_id = self.request.query_params.get('project')
        if project_id:
            queryset = queryset.filter(project_id=project_id)

        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)

        assignee_id = self.request.query_params.get('assignee')
        if assignee_id:
            queryset = queryset.filter(assignee_id=assignee_id)

        return queryset
