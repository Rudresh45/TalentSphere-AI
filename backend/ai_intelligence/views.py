from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from ai_intelligence.models import SkillGapAnalysis, LearningRecommendation
from ai_intelligence.serializers import (
    SkillGapAnalysisSerializer,
    LearningRecommendationSerializer,
    AnalyzeSkillGapRequestSerializer
)
from ai_intelligence.services import analyze_skill_gap
from employees.selectors import get_employee_by_id, get_employee_by_user_id


class SkillGapAnalysisViewSet(viewsets.ModelViewSet):
    """
    AI Skill Gap & Learning Recommendation API.
    Throttled to protect computational NLP resources.
    """
    serializer_class = SkillGapAnalysisSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'ai_throttle'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.role in ['SUPER_ADMIN', 'HR_ADMIN', 'HR_MANAGER', 'MANAGER']:
            return SkillGapAnalysis.objects.select_related('employee').prefetch_related('recommendations').all()
        if hasattr(user, 'employee_profile'):
            return SkillGapAnalysis.objects.filter(employee=user.employee_profile).prefetch_related('recommendations')
        return SkillGapAnalysis.objects.none()

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def analyze(self, request):
        """
        POST /api/v1/ai/analyze/
        Triggers AI Skill Gap analysis & generates course recommendations.
        """
        serializer = AnalyzeSkillGapRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        emp_id = serializer.validated_data.get('employee_id')
        if emp_id:
            employee = get_employee_by_id(emp_id)
        else:
            employee = get_employee_by_user_id(request.user.id)

        if not employee:
            return Response(
                {"success": False, "message": "Valid employee record required for analysis.", "error_code": "NOT_FOUND"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            analysis = analyze_skill_gap(
                employee=employee,
                target_role=serializer.validated_data['target_role'],
                required_skills=serializer.validated_data['required_skills']
            )
            return Response(
                {
                    "success": True,
                    "message": "AI Skill Gap Analysis completed.",
                    "data": SkillGapAnalysisSerializer(analysis).data
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"success": False, "message": str(e), "error_code": "AI_ANALYSIS_FAILED"},
                status=status.HTTP_400_BAD_REQUEST
            )


class RecommendationListView(generics.ListAPIView):
    """
    GET /api/v1/ai/recommendations/
    Retrieve personalized learning recommendations.
    """
    serializer_class = LearningRecommendationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'employee_profile'):
            return LearningRecommendation.objects.filter(analysis__employee=user.employee_profile)
        return LearningRecommendation.objects.none()
