from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from .forms import LoginForm, ChangePasswordForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                # Audit logging (we can import local to avoid loops)
                try:
                    from apps.auditlogs.models import AuditLog
                    # Extract IP address
                    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                    ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
                    AuditLog.objects.create(
                        user=user,
                        action='Login',
                        ip_address=ip
                    )
                except Exception:
                    pass
                messages.success(request, f"Welcome back, {user.email}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    user = request.user
    if user.is_authenticated:
        try:
            from apps.auditlogs.models import AuditLog
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
            AuditLog.objects.create(
                user=user,
                action='Logout',
                ip_address=ip
            )
        except Exception:
            pass
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


@login_required
def dashboard_view(request):
    user = request.user
    if user.role in ('Super Admin', 'HR Manager'):
        return admin_dashboard(request)
    else:
        return employee_dashboard(request)


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            if user.check_password(form.cleaned_data['old_password']):
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password updated successfully!")
                return redirect('dashboard')
            else:
                messages.error(request, "Incorrect current password.")
    else:
        form = ChangePasswordForm()
    return render(request, 'accounts/change_password.html', {'form': form})


def admin_dashboard(request):
    # Local imports to avoid circular reference
    from apps.employees.models import Employee
    from apps.leaves.models import LeaveRequest
    from apps.payroll.models import Payroll
    from apps.attendance.models import Attendance
    from apps.recruitment.models import Candidate

    today = timezone.localdate()
    
    total_employees = Employee.objects.count()
    active_employees = Employee.objects.filter(employment_status='Active').count()
    pending_leaves = LeaveRequest.objects.filter(status='Pending').count()
    
    # Payroll summary for current month
    payroll_sum = 0
    recent_payroll = Payroll.objects.filter(month=today.month, year=today.year)
    for p in recent_payroll:
        payroll_sum += p.net_salary

    # Attendance summary today
    present_today = Attendance.objects.filter(date=today, status='Present').count()
    absent_today = Attendance.objects.filter(date=today, status='Absent').count()
    
    # Recruitment pipeline
    candidates_count = Candidate.objects.count()
    screening_count = Candidate.objects.filter(status='Screening').count()
    interview_count = Candidate.objects.filter(status='Interview').count()

    context = {
        'total_employees': total_employees,
        'active_employees': active_employees,
        'pending_leaves': pending_leaves,
        'payroll_sum': payroll_sum,
        'present_today': present_today,
        'absent_today': absent_today,
        'candidates_count': candidates_count,
        'screening_count': screening_count,
        'interview_count': interview_count,
    }
    return render(request, 'dashboards/admin_dashboard.html', context)


def employee_dashboard(request):
    # Local imports
    from apps.employees.models import Employee
    from apps.leaves.models import LeaveBalance, LeaveRequest
    from apps.holidays.models import Holiday
    from apps.notifications.models import Notification
    from apps.payroll.models import Payroll
    from apps.attendance.models import Attendance

    user = request.user
    today = timezone.localdate()
    
    # Get employee profile
    employee = getattr(user, 'employee_profile', None)
    
    attendance_today = None
    leave_balances = []
    recent_notifications = []
    payslips = []
    upcoming_holidays = Holiday.objects.filter(date__gte=today).order_code = 'date'[:5] # Ordering handled in query
    upcoming_holidays = Holiday.objects.filter(date__gte=today).order_by('date')[:5]

    if employee:
        attendance_today = Attendance.objects.filter(employee=employee, date=today).first()
        leave_balances = LeaveBalance.objects.filter(employee=employee)
        payslips = Payroll.objects.filter(employee=employee).order_by('-year', '-month')[:6]

    recent_notifications = Notification.objects.filter(recipient=user).order_by('-created_at')[:5]

    context = {
        'employee': employee,
        'attendance_today': attendance_today,
        'leave_balances': leave_balances,
        'upcoming_holidays': upcoming_holidays,
        'recent_notifications': recent_notifications,
        'payslips': payslips,
    }
    return render(request, 'dashboards/employee_dashboard.html', context)
