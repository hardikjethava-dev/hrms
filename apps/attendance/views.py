from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Attendance
from services import attendance_service
from apps.employees.models import Employee


@login_required
def attendance_list(request):
    user = request.user
    is_manager = user.role in ('Super Admin', 'HR Manager')
    
    # Query parameters
    emp_id = request.GET.get('employee', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    
    if is_manager:
        attendances = Attendance.objects.all().select_related('employee', 'employee__department')
        if emp_id:
            attendances = attendances.filter(employee_id=emp_id)
    else:
        employee = getattr(user, 'employee_profile', None)
        if employee:
            attendances = Attendance.objects.filter(employee=employee)
        else:
            attendances = Attendance.objects.none()

    if start_date:
        attendances = attendances.filter(date__gte=start_date)
    if end_date:
        attendances = attendances.filter(date__lte=end_date)
        
    attendances = attendances.order_by('-date')
    
    employees = Employee.objects.all() if is_manager else []
    
    return render(request, 'attendance/attendance_list.html', {
        'attendances': attendances,
        'employees': employees,
        'is_manager': is_manager,
        'emp_filter': emp_id,
        'start_date': start_date,
        'end_date': end_date
    })


@login_required
def clock_in(request):
    if request.method == 'POST':
        employee = getattr(request.user, 'employee_profile', None)
        if not employee:
            messages.error(request, "Only employees with active profiles can clock in.")
            return redirect('dashboard')
        try:
            attendance_service.record_check_in(employee)
            messages.success(request, "Successfully checked in!")
        except Exception as e:
            messages.error(request, str(e))
    return redirect('dashboard')


@login_required
def clock_out(request):
    if request.method == 'POST':
        employee = getattr(request.user, 'employee_profile', None)
        if not employee:
            messages.error(request, "Only employees with active profiles can clock out.")
            return redirect('dashboard')
        try:
            attendance_service.record_check_out(employee)
            messages.success(request, "Successfully checked out!")
        except Exception as e:
            messages.error(request, str(e))
    return redirect('dashboard')
