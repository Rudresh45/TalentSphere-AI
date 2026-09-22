from rest_framework import serializers
from ai_intelligence.models import SkillGapAnalysis, LearningRecommendation


class LearningRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningRecommendation
        fields = ('id', 'skill_gap', 'course_title', 'description', 'priority', 'recommended_url', 'created_at')


class SkillGapAnalysisSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    recommendations = LearningRecommendationSerializer(many=True, read_only=True)

    class Meta:
        model = SkillGapAnalysis
        fields = (
            'id', 'employee', 'employee_name', 'target_role', 'match_percentage',
            'matched_skills', 'missing_skills', 'recommendations', 'created_at'
        )


class AnalyzeSkillGapRequestSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField(required=False, help_text="Employee PK to analyze. Defaults to current user employee.")
    target_role = serializers.CharField(required=True, help_text="Target role title e.g. Senior Backend Engineer")
    required_skills = serializers.ListField(
        child=serializers.CharField(),
        required=True,
        help_text="List of required skills for target role e.g. ['Python', 'FastAPI', 'Docker', 'AWS']"
    )
