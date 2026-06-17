import sys
import os
import django
from datetime import date, time

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.departments.models import Department
from apps.shifts.models import Shift
from apps.employees.models import Employee
from apps.leaves.models import LeaveType, LeaveBalance
from services.employee_service import create_employee

User = get_user_model()

def seed():
    print("Starting database seeding...")
    
    # 1. Create Departments
    hr_dept, _ = Department.objects.get_or_create(
        code='HR01',
        defaults={'name': 'Human Resources', 'description': 'HR and Administration'}
    )
    it_dept, _ = Department.objects.get_or_create(
        code='IT01',
        defaults={'name': 'Information Technology', 'description': 'IT and Development'}
    )
    finance_dept, _ = Department.objects.get_or_create(
        code='FI01',
        defaults={'name': 'Finance', 'description': 'Accounts and Finance'}
    )
    
    # 2. Create Shift
    shift, _ = Shift.objects.get_or_create(
        name='Day Shift',
        defaults={
            'start_time': time(9, 0),
            'end_time': time(18, 0),
            'grace_minutes': 15
        }
    )
    
    # 3. Create Super Admin/HR Admin User and Profile
    admin_email = 'hr.admin@yopmail.com'
    admin_password = 'admin@123'
    
    if not User.objects.filter(email=admin_email).exists():
        print(f"Creating Super Admin user: {admin_email}...")
        
        # We want this user to be is_staff=True, is_superuser=True
        # We can create Employee via service and then elevate User permissions
        admin_emp_data = {
            'employee_id': 'EMP001',
            'first_name': 'Hardik',
            'last_name': 'Jethava',
            'joining_date': date(2026, 1, 1),
            'designation': 'HR Director',
            'department': hr_dept,
        }
        admin_emp = create_employee(admin_email, admin_password, 'Super Admin', admin_emp_data)
        
        # Elevate permissions
        admin_user = admin_emp.user
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        print("Super Admin user created and elevated successfully!")
    else:
        print(f"Super Admin user {admin_email} already exists.")

    # 4. Create Normal Employee User and Profile
    emp_email = 'employee@yopmail.com'
    emp_password = 'employee@123'
    
    if not User.objects.filter(email=emp_email).exists():
        print(f"Creating Normal Employee user: {emp_email}...")
        emp_data = {
            'employee_id': 'EMP002',
            'first_name': 'John',
            'last_name': 'Doe',
            'joining_date': date(2026, 1, 15),
            'designation': 'Software Engineer',
            'department': it_dept,
        }
        create_employee(emp_email, emp_password, 'Employee', emp_data)
        print("Normal Employee user created successfully!")
    else:
        print(f"Normal Employee user {emp_email} already exists.")

    print("Seeding completed successfully!")

if __name__ == '__main__':
    seed()
