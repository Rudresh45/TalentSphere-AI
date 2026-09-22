from django.db import models
from employees.models import Employee


class AttendanceStatus(models.TextChoices):
    PRESENT = 'PRESENT', 'Present'
    ABSENT = 'ABSENT', 'Absent'
    ON_LEAVE = 'ON_LEAVE', 'On Leave'
    HALF_DAY = 'HALF_DAY', 'Half Day'


class AttendanceRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(db_index=True)
    clock_in = models.DateTimeField(null=True, blank=True)
    clock_out = models.DateTimeField(null=True, blank=True)
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    overtime_hours = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    late_arrival = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20, choices=AttendanceStatus.choices, default=AttendanceStatus.PRESENT, db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        unique_together = ('employee', 'date')
        indexes = [
            models.Index(fields=['employee', 'date']),
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return f"{self.employee.full_name} - {self.date} [{self.get_status_display()}]"


class BreakRecord(models.Model):
    attendance = models.ForeignKey(AttendanceRecord, on_delete=models.CASCADE, related_name='breaks')
    break_start = models.DateTimeField()
    break_end = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(default=0)

    def __str__(self):
        return f"Break for {self.attendance.employee.full_name} on {self.attendance.date}"
