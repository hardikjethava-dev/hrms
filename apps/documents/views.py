from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import EmployeeDocument
from .forms import EmployeeDocumentForm


def is_hr_or_admin(user):
    return user.role in ('Super Admin', 'HR Manager')


@login_required
def document_list(request):
    user = request.user
    is_mgr = is_hr_or_admin(user)
    
    if is_mgr:
        documents = EmployeeDocument.objects.all().select_related('employee')
    else:
        employee = getattr(user, 'employee_profile', None)
        if employee:
            documents = EmployeeDocument.objects.filter(employee=employee)
        else:
            documents = EmployeeDocument.objects.none()
            
    return render(request, 'documents/document_list.html', {
        'documents': documents,
        'is_manager': is_mgr
    })


@login_required
def document_upload(request):
    if not is_hr_or_admin(request.user):
        return HttpResponseForbidden("Not authorized.")
        
    if request.method == 'POST':
        form = EmployeeDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Document uploaded successfully!")
            return redirect('document_list')
    else:
        form = EmployeeDocumentForm()
    return render(request, 'documents/document_form.html', {'form': form, 'title': 'Upload Document'})


@login_required
def document_delete(request, pk):
    if not is_hr_or_admin(request.user):
        return HttpResponseForbidden("Not authorized.")
        
    doc = get_object_or_404(EmployeeDocument, pk=pk)
    doc.file.delete() # clean up files
    doc.delete()
    messages.warning(request, "Document deleted.")
    return redirect('document_list')
