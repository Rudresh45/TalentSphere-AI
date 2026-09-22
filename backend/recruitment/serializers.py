from rest_framework import serializers
from recruitment.models import JobPosition, Candidate, Application, InterviewSchedule, InterviewFeedback


class JobPositionSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    applications_count = serializers.IntegerField(source='applications.count', read_only=True)

    class Meta:
        model = JobPosition
        fields = (
            'id', 'title', 'code', 'department', 'department_name',
            'description', 'required_skills', 'min_experience', 'salary_range',
            'status', 'applications_count', 'created_at'
        )


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'resume_url', 'skills', 'experience_years', 'created_at')


class ApplicationSerializer(serializers.ModelSerializer):
    job_detail = JobPositionSerializer(source='job', read_only=True)
    candidate_detail = CandidateSerializer(source='candidate', read_only=True)

    class Meta:
        model = Application
        fields = ('id', 'job', 'job_detail', 'candidate', 'candidate_detail', 'status', 'notes', 'applied_at', 'updated_at')


class InterviewScheduleSerializer(serializers.ModelSerializer):
    interviewer_name = serializers.CharField(source='interviewer.full_name', read_only=True)
    candidate_name = serializers.CharField(source='application.candidate.__str__', read_only=True)

    class Meta:
        model = InterviewSchedule
        fields = (
            'id', 'application', 'candidate_name', 'interviewer', 'interviewer_name',
            'scheduled_time', 'meeting_link', 'round_name', 'is_completed', 'created_at'
        )


class InterviewFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewFeedback
        fields = ('id', 'interview', 'score', 'comments', 'recommendation', 'created_at')
