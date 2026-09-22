from rest_framework import serializers
from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    assignee_name = serializers.CharField(source='assignee.full_name', read_only=True)
    reporter_name = serializers.CharField(source='reporter.full_name', read_only=True)
    project_code = serializers.CharField(source='project.code', read_only=True)

    class Meta:
        model = Task
        fields = (
            'id', 'project', 'project_code', 'title', 'description',
            'assignee', 'assignee_name', 'reporter', 'reporter_name',
            'status', 'priority', 'estimated_hours', 'logged_hours',
            'due_date', 'created_at', 'updated_at'
        )
