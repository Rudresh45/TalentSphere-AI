from rest_framework import serializers
from attendance.models import AttendanceRecord, BreakRecord


class BreakRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BreakRecord
        fields = ('id', 'break_start', 'break_end', 'duration_minutes')


class AttendanceRecordSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    employee_code = serializers.CharField(source='employee.employee_id', read_only=True)
    breaks = BreakRecordSerializer(many=True, read_only=True)

    class Meta:
        model = AttendanceRecord
        fields = (
            'id', 'employee', 'employee_name', 'employee_code', 'date',
            'clock_in', 'clock_out', 'total_hours', 'overtime_hours',
            'late_arrival', 'status', 'breaks', 'created_at'
        )
