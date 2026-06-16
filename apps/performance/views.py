from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import PerformanceReview
from .forms import PerformanceReviewForm


def is_manager_or_reviewer(user):
    return user.role in ('Super Admin', 'HR Manager', 'Department Manager')


@login_required
def performance_list(request):
    user = request.user
    is_mgr = is_manager_or_reviewer(user)
    
    if is_mgr:
        # Managers can see all reviews
        reviews = PerformanceReview.objects.all().select_related('employee', 'reviewer')
    else:
        employee = getattr(user, 'employee_profile', None)
        if employee:
            reviews = PerformanceReview.objects.filter(employee=employee).select_related('reviewer')
        else:
            reviews = PerformanceReview.objects.none()
            
    return render(request, 'performance/performance_list.html', {
        'reviews': reviews,
        'is_manager': is_mgr
    })


@login_required
def performance_manage(request, pk=None):
    if not is_manager_or_reviewer(request.user):
        return HttpResponseForbidden("Not authorized.")
        
    review = get_object_or_404(PerformanceReview, pk=pk) if pk else None
    
    if request.method == 'POST':
        form = PerformanceReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Performance review saved successfully.")
            return redirect('performance_list')
    else:
        form = PerformanceReviewForm(instance=review)
        
    return render(request, 'performance/performance_form.html', {
        'form': form,
        'title': 'Edit Performance Review' if pk else 'New Performance Review'
    })
