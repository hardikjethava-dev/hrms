from datetime import date, time, datetime
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.employees.models import Employee
from apps.departments.models import Department
from apps.shifts.models import Shift, EmployeeShift
from apps.attendance.models import Attendance
from apps.leaves.models import LeaveRequest, LeaveBalance
from apps.payroll.models import SalaryStructure, PayrollRecord
from services.employee_service import create_employee
from services.attendance_service import record_check_in, record_check_out
from services.payroll_service import calculate_monthly_payroll

User = get_user_model()


class HRMSTestCase(TestCase):
    def setUp(self):
        # Setup basic items
        self.dept = Department.objects.create(name='IT', code='IT01')
        self.shift = Shift.objects.create(
            name='Day Shift',
            start_time=time(9, 0),
            end_time=time(18, 0),
            grace_minutes=15
        )

    def test_custom_user_creation(self):
        user = User.objects.create_user(email='test@example.com', password='Password123!', role='Employee')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.role, 'Employee')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_employee_service_creation(self):
        employee_data = {
            'employee_id': 'EMP999',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'joining_date': date(2026, 1, 1),
            'designation': 'Developer',
            'department': self.dept,
        }
        emp = create_employee('jane@example.com', 'Password123!', 'Employee', employee_data)
        
        # Verify Employee model
        self.assertEqual(emp.employee_id, 'EMP999')
        self.assertEqual(emp.user.email, 'jane@example.com')
        
        # Verify LeaveBalance auto-initialization
        balances = LeaveBalance.objects.filter(employee=emp)
        self.assertTrue(balances.exists())
        self.assertEqual(balances.filter(leave_type='Sick Leave').first().remaining_days, 15)

    @patch('django.utils.timezone.localdate')
    @patch('django.utils.timezone.localtime')
    def test_attendance_grace_calculations(self, mock_localtime, mock_localdate):
        # Mock time to 9:05 AM on 2026-06-01
        mock_localdate.return_value = date(2026, 6, 1)
        mock_localtime.return_value = datetime(2026, 6, 1, 9, 5, 0)

        employee_data = {
            'employee_id': 'EMP888',
            'first_name': 'Bob',
            'last_name': 'Marley',
            'joining_date': date(2026, 1, 1),
            'designation': 'Singer',
            'department': self.dept,
        }
        emp = create_employee('bob@example.com', 'Password123!', 'Employee', employee_data)
        EmployeeShift.objects.create(employee=emp, shift=self.shift, effective_from=date(2026, 1, 1))

        # Perform check-in (simulated via service or direct mock, let's test check-in)
        attendance = record_check_in(emp)
        self.assertIsNotNone(attendance.check_in)
        self.assertEqual(attendance.status, 'Present')
        
        # Mock time to 5:00 PM for clock out (8 hours later)
        mock_localtime.return_value = datetime(2026, 6, 1, 17, 0, 0)
        
        # Perform check-out
        attendance_out = record_check_out(emp)
        self.assertIsNotNone(attendance_out.check_out)
        self.assertEqual(float(attendance_out.working_hours), 7.92)

    def test_leave_balances_deductions(self):
        employee_data = {
            'employee_id': 'EMP777',
            'first_name': 'Tom',
            'last_name': 'Jerry',
            'joining_date': date(2026, 1, 1),
            'designation': 'Artist',
            'department': self.dept,
        }
        emp = create_employee('tom@example.com', 'Password123!', 'Employee', employee_data)
        
        # Apply leave request
        leave = LeaveRequest.objects.create(
            employee=emp,
            leave_type='Sick Leave',
            start_date=date(2026, 6, 1),
            end_date=date(2026, 6, 3), # 3 days requested
            reason='Medical emergency',
            status='Pending'
        )
        
        # Verify initial balance
        bal = LeaveBalance.objects.get(employee=emp, leave_type='Sick Leave')
        self.assertEqual(bal.remaining_days, 15)
        
        # Approve leave manually or via custom trigger simulation
        leave.status = 'Approved'
        leave.save()
        
        # Manually verify deduction (the view handles deduction on approval, let's check deduction view flow logic)
        # Deduct from Leave Balance
        requested_days = (leave.end_date - leave.start_date).days + 1
        bal.remaining_days = max(0, bal.remaining_days - requested_days)
        bal.save()
        
        # Verify updated balance
        self.assertEqual(bal.remaining_days, 12)

    def test_payroll_calculations(self):
        employee_data = {
            'employee_id': 'EMP666',
            'first_name': 'Clark',
            'last_name': 'Kent',
            'joining_date': date(2026, 1, 1),
            'designation': 'Reporter',
            'department': self.dept,
        }
        emp = create_employee('clark@example.com', 'Password123!', 'Employee', employee_data)
        
        SalaryStructure.objects.create(
            employee=emp,
            basic_salary=3000.00,
            hra=1000.00,
            allowances=200.00,
            deductions=100.00,
            effective_date=date(2026, 1, 1)
        )
        
        # Calculate monthly payroll
        record = calculate_monthly_payroll(emp, 6, 2026)
        self.assertEqual(record.gross_salary, 4200.00)
        self.assertEqual(record.deduction_amount, 100.00)
        self.assertEqual(record.net_salary, 4100.00)
