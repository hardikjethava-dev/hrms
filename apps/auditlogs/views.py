from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import AuditLog


@login_required
def audit_list(request):
    if request.user.role != 'Super Admin':
        return HttpResponseForbidden("Not authorized.")
        
    logs = AuditLog.objects.all().select_related('user').order_by('-timestamp')
    return render(request, 'auditlogs/audit_list.html', {
        'logs': logs
    })
