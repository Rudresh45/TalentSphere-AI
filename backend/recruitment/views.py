from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from recruitment.models import JobPosition, Candidate, Application, InterviewSchedule, InterviewFeedback
from recruitment.serializers import (
    JobPositionSerializer, CandidateSerializer, ApplicationSerializer,
    InterviewScheduleSerializer, InterviewFeedbackSerializer
)
from accounts.permissions import IsRecruiter, IsHRAdmin


class JobPositionViewSet(viewsets.ModelViewSet):
    queryset = JobPosition.objects.select_related('department').all()
    serializer_class = JobPositionSerializer
    permission_classes = [IsAuthenticated, IsRecruiter]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'code', 'required_skills']


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticated, IsRecruiter]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email', 'skills']


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.select_related('job', 'candidate').all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsRecruiter]


class InterviewScheduleViewSet(viewsets.ModelViewSet):
    queryset = InterviewSchedule.objects.select_related('application', 'application__candidate', 'interviewer').all()
    serializer_class = InterviewScheduleSerializer
    permission_classes = [IsAuthenticated, IsRecruiter]


class InterviewFeedbackViewSet(viewsets.ModelViewSet):
    queryset = InterviewFeedback.objects.select_related('interview').all()
    serializer_class = InterviewFeedbackSerializer
    permission_classes = [IsAuthenticated, IsRecruiter]
