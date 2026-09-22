from rest_framework import serializers
from sprints.models import Sprint
from tasks.serializers import TaskSerializer


class SprintSerializer(serializers.ModelSerializer):
    project_code = serializers.CharField(source='project.code', read_only=True)
    tasks_detail = TaskSerializer(source='tasks', many=True, read_only=True)

    class Meta:
        model = Sprint
        fields = (
            'id', 'project', 'project_code', 'name', 'goal', 'start_date',
            'end_date', 'status', 'tasks', 'tasks_detail', 'created_at'
        )
