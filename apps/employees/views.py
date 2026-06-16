from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db import models
from .models import Employee
from .forms import EmployeeForm
from services import employee_service


def is_hr_or_admin(user):
    return user.is_authenticated and user.role in ('Super Admin', 'HR Manager')


@login_required
def employee_list(request):
    query = request.GET.get('q', '')
    dept = request.GET.get('dept', '')
    status = request.GET.get('status', '')
    
    employees = Employee.objects.all().select_related('user', 'department')
    if query:
        employees = employees.filter(
            models.Q(first_name__icontains=query) | 
            models.Q(last_name__icontains=query) | 
            models.Q(employee_id__icontains=query)
        )
    if dept:
        employees = employees.filter(department_id=dept)
    if status:
        employees = employees.filter(employment_status=status)

    from apps.departments.models import Department
    departments = Department.objects.all()
    
    return render(request, 'employees/employee_list.html', {
        'employees': employees,
        'departments': departments,
        'query': query,
        'dept_filter': dept,
        'status_filter': status,
        'is_manager': is_hr_or_admin(request.user)
    })


@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/employee_detail.html', {
        'employee': employee,
        'is_manager': is_hr_or_admin(request.user)
    })


@login_required
def employee_create(request):
    if not is_hr_or_admin(request.user):
        return HttpResponseForbidden("Not authorized.")
        
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            role = form.cleaned_data['role']
            password = form.cleaned_data['password'] or 'Password123!'
            
            # Clean fields mapping
            emp_fields = [f.name for f in Employee._meta.fields if f.name not in ('id', 'user', 'created_at', 'updated_at')]
            employee_data = {}
            for field in emp_fields:
                if field in form.cleaned_data:
                    employee_data[field] = form.cleaned_data[field]
            
            try:
                employee_service.create_employee(email, password, role, employee_data)
                messages.success(request, "Employee created successfully!")
                return redirect('employee_list')
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
    else:
        form = EmployeeForm()
        
    return render(request, 'employees/employee_form.html', {'form': form, 'title': 'Create Employee'})


@login_required
def employee_edit(request, pk):
    if not is_hr_or_admin(request.user):
        return HttpResponseForbidden("Not authorized.")
        
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            email = form.cleaned_data['email']
            role = form.cleaned_data['role']
            
            emp_fields = [f.name for f in Employee._meta.fields if f.name not in ('id', 'user', 'created_at', 'updated_at')]
            employee_data = {}
            for field in emp_fields:
                if field in form.cleaned_data:
                    employee_data[field] = form.cleaned_data[field]
            
            try:
                employee_service.update_employee(employee, email, role, employee_data)
                messages.success(request, "Employee updated successfully!")
                return redirect('employee_detail', pk=employee.pk)
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
    else:
        form = EmployeeForm(instance=employee, initial={
            'email': employee.user.email,
            'role': employee.user.role,
        })
        
    return render(request, 'employees/employee_form.html', {'form': form, 'title': 'Edit Employee', 'employee': employee})


@login_required
def employee_terminate(request, pk):
    if not is_hr_or_admin(request.user):
        return HttpResponseForbidden("Not authorized.")
        
    employee = get_object_or_404(Employee, pk=pk)
    employee_service.terminate_employee(employee)
    messages.warning(request, f"Employee {employee.first_name} {employee.last_name} has been terminated.")
    return redirect('employee_detail', pk=pk)
