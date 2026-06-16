from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Department
from .forms import DepartmentForm


def is_hr_or_admin(user):
    return user.is_authenticated and user.role in ('Super Admin', 'HR Manager')


@login_required
def department_list(request):
    departments = Department.objects.all().select_related('head')
    return render(request, 'departments/department_list.html', {
        'departments': departments,
        'is_manager': is_hr_or_admin(request.user)
    })


@login_required
def department_create(request):
    if not is_hr_or_admin(request.user):
        return HttpResponseForbidden("Not authorized.")
        
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Department created successfully!")
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'departments/department_form.html', {'form': form, 'title': 'Create Department'})


@login_required
def department_edit(request, pk):
    if not is_hr_or_admin(request.user):
        return HttpResponseForbidden("Not authorized.")
        
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, "Department updated successfully!")
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'departments/department_form.html', {'form': form, 'title': 'Edit Department', 'department': department})
