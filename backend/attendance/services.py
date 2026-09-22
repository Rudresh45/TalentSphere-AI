"""
TalentSphere Attendance Business Services
"""
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime, time
from attendance.models import AttendanceRecord, BreakRecord, AttendanceStatus
from employees.models import Employee


def clock_in_employee(*, employee: Employee) -> AttendanceRecord:
    """
    Clock in service for employee today.
    Enforces single clock-in per day.
    """
    today = timezone.now().date()
    existing = AttendanceRecord.objects.filter(employee=employee, date=today).first()
    if existing and existing.clock_in:
        raise ValidationError("Employee has already clocked in today.")

    now = timezone.now()
    is_late = now.time() > time(9, 30)  # Standard start time 09:30 AM

    if not existing:
        record = AttendanceRecord.objects.create(
            employee=employee,
            date=today,
            clock_in=now,
            late_arrival=is_late,
            status=AttendanceStatus.PRESENT
        )
    else:
        existing.clock_in = now
        existing.late_arrival = is_late
        existing.save()
        record = existing

    return record


def clock_out_employee(*, employee: Employee) -> AttendanceRecord:
    """
    Clock out service for employee today.
    Calculates total hours and overtime.
    """
    today = timezone.now().date()
    record = AttendanceRecord.objects.filter(employee=employee, date=today).first()
    if not record or not record.clock_in:
        raise ValidationError("Cannot clock out without clocking in first.")

    now = timezone.now()
    record.clock_out = now

    # Calculate duration
    duration_seconds = (now - record.clock_in).total_seconds()
    hours = round(duration_seconds / 3600.0, 2)
    record.total_hours = hours

    # Standard shift is 8 hours
    if hours > 8.0:
        record.overtime_hours = round(hours - 8.0, 2)

    record.save()
    return record


def start_break(*, employee: Employee) -> BreakRecord:
    """Start break for employee today."""
    today = timezone.now().date()
    attendance = AttendanceRecord.objects.filter(employee=employee, date=today).first()
    if not attendance or not attendance.clock_in:
        raise ValidationError("Must be clocked in to take a break.")

    # Check for active break
    active_break = BreakRecord.objects.filter(attendance=attendance, break_end__isnull=True).first()
    if active_break:
        raise ValidationError("An active break is already in progress.")

    return BreakRecord.objects.create(
        attendance=attendance,
        break_start=timezone.now()
    )


def end_break(*, employee: Employee) -> BreakRecord:
    """End active break for employee today."""
    today = timezone.now().date()
    attendance = AttendanceRecord.objects.filter(employee=employee, date=today).first()
    if not attendance:
        raise ValidationError("No attendance record found for today.")

    active_break = BreakRecord.objects.filter(attendance=attendance, break_end__isnull=True).first()
    if not active_break:
        raise ValidationError("No active break to end.")

    now = timezone.now()
    active_break.break_end = now
    duration = int((now - active_break.break_start).total_seconds() / 60)
    active_break.duration_minutes = duration
    active_break.save()
    return active_break
