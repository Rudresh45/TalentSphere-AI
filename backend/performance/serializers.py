from rest_framework import serializers
from performance.models import PerformanceReview


class PerformanceReviewSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    reviewer_name = serializers.CharField(source='reviewer.full_name', read_only=True)

    class Meta:
        model = PerformanceReview
        fields = (
            'id', 'employee', 'employee_name', 'reviewer', 'reviewer_name',
            'review_period', 'score', 'strengths', 'areas_for_improvement',
            'goals', 'created_at'
        )
