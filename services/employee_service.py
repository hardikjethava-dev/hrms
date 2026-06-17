from django.db import transaction
from django.contrib.auth import get_user_model
from apps.employees.models import Employee
from apps.leaves.models import LeaveBalance # We can initialize leave balance on employee creation

User = get_user_model()

@transaction.atomic
def create_employee(user_email, password, role, employee_data):
    """
    Creates a User account and the corresponding Employee profile.
    Additionally, sets up default leave balances for the new employee.
    """
    # 1. Create the custom User
    user = User.objects.create_user(
        email=user_email,
        password=password,
        role=role,
        employee_code=employee_data.get('employee_id')
    )
    
    # 2. Create the Employee profile
    employee_data.pop('email', None)
    personal_email = employee_data.pop('personal_email', user_email)
    employee = Employee.objects.create(
        user=user,
        personal_email=personal_email,
        **employee_data
    )
    
    # 3. Initialize Leave Balances
    leave_types = ['Annual Leave', 'Sick Leave', 'Casual Leave', 'Maternity Leave', 'Paternity Leave', 'Unpaid Leave']
    for lt in leave_types:
        try:
            from apps.leaves.models import LeaveBalance, LeaveType
            # Determine appropriate base days
            allowed = 15 if 'Sick' in lt or 'Casual' in lt else (20 if 'Annual' in lt else 0)
            leave_type_obj, _ = LeaveType.objects.get_or_create(
                name=lt,
                defaults={'days_per_year': allowed, 'is_paid': lt != 'Unpaid Leave'}
            )
            LeaveBalance.objects.get_or_create(
                employee=employee,
                leave_type=leave_type_obj,
                defaults={'allowed_days': allowed, 'remaining_days': allowed}
            )
        except Exception:
            pass
            
    return employee


@transaction.atomic
def update_employee(employee, user_email, role, employee_data):
    """
    Updates the Employee profile and corresponding User.
    """
    user = employee.user
    user.email = user_email
    user.role = role
    user.employee_code = employee_data.get('employee_id', user.employee_code)
    user.save()
    
    employee_data.pop('email', None)
    personal_email = employee_data.pop('personal_email', user_email)
    for key, value in employee_data.items():
        setattr(employee, key, value)
    employee.personal_email = personal_email
    employee.save()
    return employee


@transaction.atomic
def terminate_employee(employee):
    """
    Terminates an employee: sets status to Terminated, and deactivates User.
    """
    employee.employment_status = 'Terminated'
    employee.save()
    
    user = employee.user
    user.is_active = False
    user.save()
    return employee
