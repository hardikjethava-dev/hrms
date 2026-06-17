from decimal import Decimal
from django.utils import timezone
from apps.payroll.models import SalaryStructure, Payroll
from apps.leaves.models import LeaveRequest


def calculate_monthly_payroll(employee, month, year):
    """
    Computes compensation figures, deducts any unpaid leave days,
    and saves/updates the monthly Payroll.
    """
    # 1. Fetch active salary structure
    structure = getattr(employee, 'salary_structure', None)
    if not structure:
        raise ValueError(f"Employee {employee} does not have an active Salary Structure defined.")
        
    basic = Decimal(str(structure.base_salary))
    hra = Decimal(str(structure.hra))
    allowances = Decimal(str(structure.allowances))
    fixed_deductions = Decimal(str(structure.deductions))
    
    # 2. Calculate Unpaid Leaves
    # Count approved 'Unpaid Leave' days falling inside the target month & year
    unpaid_leaves = LeaveRequest.objects.filter(
        employee=employee,
        leave_type__name='Unpaid Leave',
        status='Approved',
        start_date__year=year,
        start_date__month=month
    )
    
    unpaid_days = 0
    for leave in unpaid_leaves:
        # Simple duration calculation within boundaries
        duration = (leave.end_date - leave.start_date).days + 1
        unpaid_days += duration
        
    # Deduct per-day basic rate for unpaid days (assuming 30-day month)
    daily_rate = basic / Decimal(30.0)
    leave_deduction = daily_rate * Decimal(unpaid_days)
    
    # 3. Sum salaries
    gross_salary = basic + hra + allowances
    total_deductions = fixed_deductions + leave_deduction
    net_salary = max(Decimal(0.00), gross_salary - total_deductions)
    
    # 4. Save record
    record, created = Payroll.objects.update_or_create(
        employee=employee,
        month=month,
        year=year,
        defaults={
            'gross_salary': round(gross_salary, 2),
            'total_deductions': round(total_deductions, 2),
            'net_salary': round(net_salary, 2),
            'generated_at': timezone.now()
        }
    )
    
    # Trigger Notification for payroll generation (local import inside signal)
    try:
        from apps.notifications.models import Notification
        Notification.objects.create(
            recipient=employee.user,
            title="Payslip Generated",
            message=f"Your payslip for {record.get_month_display()} {record.year} is now available."
        )
    except Exception:
        pass
        
    return record
