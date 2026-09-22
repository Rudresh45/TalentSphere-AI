from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from performance.models import PerformanceReview
from performance.serializers import PerformanceReviewSerializer
from tasks.models import Task, TaskStatus
from attendance.models import AttendanceRecord, AttendanceStatus
from employees.models import Employee
from django.db.models import Count, Q, Avg


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = PerformanceReview.objects.select_related('employee', 'reviewer').all()
    serializer_class = PerformanceReviewSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def dashboard(self, request):
        """
        GET /api/v1/performance/dashboard/
        KPI Analytics Engine returning productivity metrics.
        """
        total_tasks = Task.objects.count()
        completed_tasks = Task.objects.filter(status=TaskStatus.COMPLETED).count()
        in_progress_tasks = Task.objects.filter(status=TaskStatus.IN_PROGRESS).count()
        blocked_tasks = Task.objects.filter(status=TaskStatus.BLOCKED).count()

        completion_rate = round((completed_tasks / total_tasks * 100), 2) if total_tasks > 0 else 0.0

        total_attendance = AttendanceRecord.objects.count()
        present_count = AttendanceRecord.objects.filter(status=AttendanceStatus.PRESENT).count()
        attendance_percentage = round((present_count / total_attendance * 100), 2) if total_attendance > 0 else 0.0

        avg_review_score = PerformanceReview.objects.aggregate(avg=Avg('score'))['avg'] or 0.0

        return Response({
            "success": True,
            "data": {
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "in_progress_tasks": in_progress_tasks,
                "blocked_tasks": blocked_tasks,
                "task_completion_rate": completion_rate,
                "attendance_percentage": attendance_percentage,
                "average_performance_score": round(float(avg_review_score), 2)
            }
        }, status=status.HTTP_200_OK)
