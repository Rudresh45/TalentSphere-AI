from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ai_intelligence.views import SkillGapAnalysisViewSet, RecommendationListView

app_name = 'ai_intelligence'

router = DefaultRouter()
router.register(r'skill-gap', SkillGapAnalysisViewSet, basename='skill_gap')

urlpatterns = [
    path('recommendations/', RecommendationListView.as_view(), name='recommendation_list'),
    path('', include(router.urls)),
]
