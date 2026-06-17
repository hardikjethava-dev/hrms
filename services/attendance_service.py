from datetime import datetime, date, time, timedelta
from django.utils import timezone
from apps.attendance.models import Attendance
from apps.shifts.models import EmployeeShift, Shift


def get_decimal_hours(start_time, end_time):
    dummy_date = date(2000, 1, 1)
    dt1 = datetime.combine(dummy_date, start_time)
    dt2 = datetime.combine(dummy_date, end_time)
    if dt2 < dt1:
        dt2 += timedelta(days=1)
    delta = dt2 - dt1
    return round(delta.total_seconds() / 3600.0, 2)


def get_employee_shift_for_date(employee, eval_date):
    """
    Finds the active shift for the employee on a given date.
    Returns default shift (09:00 - 18:00) if none assigned.
    """
    emp_shift = EmployeeShift.objects.filter(
        employee=employee,
        effective_from__lte=eval_date
    ).order_by('-effective_from').first()
    
    if emp_shift:
        return emp_shift.shift
        
    # Standard default fallback
    default_shift, _ = Shift.objects.get_or_create(
        name="Standard Day Shift",
        defaults={
            'start_time': time(9, 0),
            'end_time': time(18, 0),
            'grace_minutes': 15
        }
    )
    return default_shift


def record_check_in(employee):
    """
    Records a clock-in for the employee on timezone.localdate().
    Calculates if the check-in is late compared to the shift start time.
    """
    today = timezone.localdate()
    now_time = timezone.localtime().time()
    
    # Check if attendance already exists
    attendance, created = Attendance.objects.get_or_create(
        employee=employee,
        date=today,
        defaults={'status': 'Present'}
    )
    
    if attendance.check_in is not None:
        raise ValueError("Already checked in today.")
        
    shift = get_employee_shift_for_date(employee, today)
    
    # Calculate if late
    shift_datetime = datetime.combine(today, shift.start_time)
    grace_datetime = shift_datetime + timedelta(minutes=shift.grace_minutes)
    checkin_datetime = datetime.combine(today, now_time)
    
    remarks = ""
    status = 'Present'
    if checkin_datetime > grace_datetime:
        remarks = f"Late check-in by {round((checkin_datetime - shift_datetime).total_seconds() / 60)} minutes."
        # If checked in after 2 hours, mark as Half Day
        if checkin_datetime > shift_datetime + timedelta(hours=2):
            status = 'Half Day'
            remarks += " Late check-in beyond 2 hours limit."

    attendance.check_in = now_time
    attendance.status = status
    attendance.remarks = remarks
    attendance.save()
    return attendance


def record_check_out(employee):
    """
    Records clock-out for today, calculates working hours, overtime, and final status.
    """
    today = timezone.localdate()
    now_time = timezone.localtime().time()
    
    attendance = Attendance.objects.filter(employee=employee, date=today).first()
    if not attendance or attendance.check_in is None:
        raise ValueError("Cannot clock out without clocking in first.")
        
    if attendance.check_out is not None:
        raise ValueError("Already clocked out today.")
        
    attendance.check_out = now_time
    
    # Calculate decimal hours
    hours = get_decimal_hours(attendance.check_in, now_time)
    attendance.working_hours = hours
    
    # Calculate overtime hours (hours worked past 8 hours standard)
    if hours > 8.0:
        attendance.overtime_hours = round(hours - 8.0, 2)
    else:
        attendance.overtime_hours = 0.0
    
    # Status rules based on hours worked
    remarks = attendance.remarks
    status = attendance.status
    
    if hours < 1.0:
        status = 'Absent'
        remarks += f" Clock-out early. Worked only {hours} hrs."
    elif hours < 4.0:
        status = 'Half Day'
        remarks += f" Worked only {hours} hrs (under 4 hours limit)."
    elif hours < 8.0 and status == 'Present':
        # Let's keep status as Present, but record comments
        remarks += f" Left early. Worked {hours} hrs."
        
    attendance.status = status
    attendance.remarks = remarks
    attendance.save()
    return attendance
