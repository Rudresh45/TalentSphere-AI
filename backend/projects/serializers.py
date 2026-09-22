from rest_framework import serializers
from projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.full_name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    tasks_count = serializers.IntegerField(source='tasks.count', read_only=True)

    class Meta:
        model = Project
        fields = (
            'id', 'name', 'code', 'description', 'department', 'department_name',
            'owner', 'owner_name', 'members', 'status', 'start_date', 'end_date',
            'tasks_count', 'created_at', 'updated_at'
        )
