from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseForbidden
from .models import LeaveRequest, LeaveBalance
from .forms import LeaveRequestForm
from apps.employees.models import Employee


def is_hr_or_manager(user):
    return user.role in ('Super Admin', 'HR Manager', 'Department Manager')


@login_required
def leave_list(request):
    user = request.user
    is_mgr = is_hr_or_manager(user)
    
    if is_mgr:
        # Managers view all requests
        pending_requests = LeaveRequest.objects.filter(status='Pending').select_related('employee', 'employee__department')
        history_requests = LeaveRequest.objects.exclude(status='Pending').select_related('employee', 'employee__department').order_by('-created_at')
        balances = []
    else:
        employee = getattr(user, 'employee_profile', None)
        if employee:
            pending_requests = LeaveRequest.objects.filter(employee=employee, status='Pending')
            history_requests = LeaveRequest.objects.filter(employee=employee).exclude(status='Pending').order_by('-created_at')
            balances = LeaveBalance.objects.filter(employee=employee)
        else:
            pending_requests = LeaveRequest.objects.none()
            history_requests = LeaveRequest.objects.none()
            balances = []

    return render(request, 'leaves/leave_list.html', {
        'pending_requests': pending_requests,
        'history_requests': history_requests,
        'balances': balances,
        'is_manager': is_mgr
    })


@login_required
def leave_apply(request):
    employee = getattr(request.user, 'employee_profile', None)
    if not employee:
        messages.error(request, "Only employees with active profiles can apply for leave.")
        return redirect('leave_list')

    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = employee
            leave.status = 'Pending'
            leave.save()
            messages.success(request, "Leave request submitted successfully!")
            return redirect('leave_list')
    else:
        form = LeaveRequestForm()
    return render(request, 'leaves/leave_form.html', {'form': form, 'title': 'Apply for Leave'})


@login_required
def leave_approve(request, pk):
    if not is_hr_or_manager(request.user):
        return HttpResponseForbidden("Not authorized.")

    manager_employee = getattr(request.user, 'employee_profile', None)
    leave = get_object_or_404(LeaveRequest, pk=pk)
    
    if leave.status != 'Pending':
        messages.error(request, "Leave request is already processed.")
        return redirect('leave_list')

    # Calculate requested days
    requested_days = (leave.end_date - leave.start_date).days + 1
    
    # Deduct from Leave Balance
    balance = LeaveBalance.objects.filter(employee=leave.employee, leave_type=leave.leave_type).first()
    if balance:
        if balance.remaining_days < requested_days and leave.leave_type != 'Unpaid Leave':
            messages.warning(request, f"Employee has only {balance.remaining_days} remaining days. Approving anyway.")
        
        balance.remaining_days = max(0, balance.remaining_days - requested_days)
        balance.save()

    leave.status = 'Approved'
    leave.approved_by = manager_employee
    leave.approved_at = timezone.now()
    leave.save()
    
    messages.success(request, f"Leave request for {leave.employee} approved successfully.")
    return redirect('leave_list')


@login_required
def leave_reject(request, pk):
    if not is_hr_or_manager(request.user):
        return HttpResponseForbidden("Not authorized.")

    manager_employee = getattr(request.user, 'employee_profile', None)
    leave = get_object_or_404(LeaveRequest, pk=pk)
    
    if leave.status != 'Pending':
        messages.error(request, "Leave request is already processed.")
        return redirect('leave_list')

    leave.status = 'Rejected'
    leave.approved_by = manager_employee
    leave.approved_at = timezone.now()
    leave.save()
    
    messages.warning(request, f"Leave request for {leave.employee} rejected.")
    return redirect('leave_list')


@login_required
def leave_cancel(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    
    # Verify owner
    if leave.employee.user != request.user:
        return HttpResponseForbidden("Not authorized to cancel this request.")

    if leave.status != 'Pending':
        messages.error(request, "Cannot cancel a processed leave request.")
        return redirect('leave_list')

    leave.status = 'Cancelled'
    leave.save()
    
    messages.info(request, "Leave request has been cancelled.")
    return redirect('leave_list')
