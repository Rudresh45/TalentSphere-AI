from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recruitment.views import (
    JobPositionViewSet, CandidateViewSet, ApplicationViewSet,
    InterviewScheduleViewSet, InterviewFeedbackViewSet
)

app_name = 'recruitment'

router = DefaultRouter()
router.register(r'jobs', JobPositionViewSet, basename='job')
router.register(r'candidates', CandidateViewSet, basename='candidate')
router.register(r'applications', ApplicationViewSet, basename='application')
router.register(r'interviews', InterviewScheduleViewSet, basename='interview')
router.register(r'feedback', InterviewFeedbackViewSet, basename='feedback')

urlpatterns = [
    path('', include(router.urls)),
]
