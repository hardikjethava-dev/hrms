from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils import timezone
from .models import Payroll, SalaryStructure
from .forms import SalaryStructureForm
from services import payroll_service
from apps.employees.models import Employee


def is_hr_or_admin(user):
    return user.role in ('Super Admin', 'HR Manager')


@login_required
def payroll_list(request):
    user = request.user
    is_mgr = is_hr_or_admin(user)
    
    if is_mgr:
        records = Payroll.objects.all().select_related('employee', 'employee__department').order_by('-year', '-month')
        structures = SalaryStructure.objects.all().select_related('employee')
    else:
        employee = getattr(user, 'employee_profile', None)
        if employee:
            records = Payroll.objects.filter(employee=employee).order_by('-year', '-month')
        else:
            records = Payroll.objects.none()
        structures = []

    return render(request, 'payroll/payroll_list.html', {
        'records': records,
        'structures': structures,
        'is_manager': is_mgr,
        'months': Payroll.MONTH_CHOICES,
        'current_year': timezone.localdate().year
    })


@login_required
def generate_payroll_view(request):
    if not is_hr_or_admin(request.user):
        return HttpResponseForbidden("Not authorized.")

    if request.method == 'POST':
        month = int(request.POST.get('month', 0))
        year = int(request.POST.get('year', 0))
        
        if not month or not year:
            messages.error(request, "Invalid month or year selected.")
            return redirect('payroll_list')
            
        employees = Employee.objects.filter(employment_status='Active')
        success_count = 0
        error_count = 0
        
        for emp in employees:
            try:
                payroll_service.calculate_monthly_payroll(emp, month, year)
                success_count += 1
            except Exception:
                error_count += 1
                
        messages.success(request, f"Payroll generation complete: {success_count} success, {error_count} failed.")
    return redirect('payroll_list')


@login_required
def salary_structure_manage(request, pk=None):
    if not is_hr_or_admin(request.user):
        return HttpResponseForbidden("Not authorized.")

    structure = get_object_or_404(SalaryStructure, pk=pk) if pk else None
    
    if request.method == 'POST':
        form = SalaryStructureForm(request.POST, instance=structure)
        if form.is_valid():
            form.save()
            messages.success(request, "Salary structure configured successfully!")
            return redirect('payroll_list')
    else:
        form = SalaryStructureForm(instance=structure)
        
    return render(request, 'payroll/salary_structure_form.html', {
        'form': form,
        'title': 'Edit Salary Structure' if pk else 'Add Salary Structure'
    })
