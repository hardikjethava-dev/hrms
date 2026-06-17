from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import JobOpening, Candidate
from .forms import JobOpeningForm, CandidateForm


def is_hr_or_admin(user):
    return user.role in ('Super Admin', 'HR Manager')


@login_required
def recruitment_list(request):
    if not is_hr_or_admin(request.user):
        return HttpResponseForbidden("Not authorized.")
        
    jobs = JobOpening.objects.all().select_related('department')
    candidates = Candidate.objects.all().select_related('job_opening')
    
    return render(request, 'recruitment/recruitment_list.html', {
        'jobs': jobs,
        'candidates': candidates
    })


@login_required
def job_create(request):
    if not is_hr_or_admin(request.user):
        return HttpResponseForbidden("Not authorized.")
        
    if request.method == 'POST':
        form = JobOpeningForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Job opening posted successfully!")
            return redirect('recruitment_list')
    else:
        form = JobOpeningForm()
    return render(request, 'recruitment/job_form.html', {'form': form, 'title': 'Create Job Opening'})


@login_required
def candidate_manage(request, pk=None):
    if not is_hr_or_admin(request.user):
        return HttpResponseForbidden("Not authorized.")
        
    candidate = get_object_or_404(Candidate, pk=pk) if pk else None
    
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES, instance=candidate)
        if form.is_valid():
            form.save()
            messages.success(request, "Candidate information saved.")
            return redirect('recruitment_list')
    else:
        form = CandidateForm(instance=candidate)
        
    return render(request, 'recruitment/candidate_form.html', {
        'form': form,
        'title': 'Edit Candidate Details' if pk else 'Add Candidate'
    })
