from django.db import transaction
from django.utils import timezone
from apps.leaves.models import LeaveRequest, LeaveBalance, LeaveType
from django.core.exceptions import ValidationError


@transaction.atomic
def apply_leave(employee, leave_data):
    """
    Submits a new leave request for approval.
    """
    leave_type = leave_data.get('leave_type')
    start_date = leave_data.get('start_date')
    end_date = leave_data.get('end_date')
    reason = leave_data.get('reason')

    if start_date and end_date and start_date > end_date:
        raise ValidationError("End date cannot be before start date.")

    request = LeaveRequest.objects.create(
        employee=employee,
        leave_type=leave_type,
        start_date=start_date,
        end_date=end_date,
        reason=reason,
        status='Pending'
    )
    return request


@transaction.atomic
def approve_leave(leave_request, manager_employee):
    """
    Approves a pending leave request and deducts remaining days from balance.
    """
    if leave_request.status != 'Pending':
        raise ValidationError("Leave request is already processed.")

    # Calculate requested days
    requested_days = (leave_request.end_date - leave_request.start_date).days + 1

    # Deduct from Leave Balance
    balance, created = LeaveBalance.objects.get_or_create(
        employee=leave_request.employee,
        leave_type=leave_request.leave_type,
        defaults={'allowed_days': leave_request.leave_type.days_per_year, 'remaining_days': leave_request.leave_type.days_per_year}
    )
    
    if balance.remaining_days < requested_days and leave_request.leave_type.is_paid:
        # We allow it but deduct (can go to negative or floor to 0 depending on logic, let's keep max(0, remaining_days - requested_days))
        balance.remaining_days = max(0, balance.remaining_days - requested_days)
    else:
        balance.remaining_days = max(0, balance.remaining_days - requested_days)
    
    balance.save()

    leave_request.status = 'Approved'
    leave_request.approved_by = manager_employee
    leave_request.approved_at = timezone.now()
    leave_request.save()
    return leave_request


@transaction.atomic
def reject_leave(leave_request, manager_employee):
    """
    Rejects a pending leave request.
    """
    if leave_request.status != 'Pending':
        raise ValidationError("Leave request is already processed.")

    leave_request.status = 'Rejected'
    leave_request.approved_by = manager_employee
    leave_request.approved_at = timezone.now()
    leave_request.save()
    return leave_request


@transaction.atomic
def cancel_leave(leave_request, user):
    """
    Cancels a pending leave request.
    """
    if leave_request.employee.user != user:
        raise ValidationError("Not authorized to cancel this request.")

    if leave_request.status != 'Pending':
        raise ValidationError("Cannot cancel a processed leave request.")

    leave_request.status = 'Cancelled'
    leave_request.save()
    return leave_request
