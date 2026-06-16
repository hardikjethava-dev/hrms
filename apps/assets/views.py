from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Asset, AssetAllocation
from .forms import AssetForm, AssetAllocationForm


def is_hr_or_admin(user):
    return user.role in ('Super Admin', 'HR Manager')


@login_required
def asset_list(request):
    user = request.user
    is_mgr = is_hr_or_admin(user)
    
    if is_mgr:
        assets = Asset.objects.all().order_by('name')
        allocations = AssetAllocation.objects.all().select_related('asset', 'employee')
    else:
        employee = getattr(user, 'employee_profile', None)
        if employee:
            allocations = AssetAllocation.objects.filter(employee=employee, returned_date__isnull=True).select_related('asset')
            assets = [alloc.asset for alloc in allocations]
        else:
            allocations = []
            assets = []

    return render(request, 'assets/asset_list.html', {
        'assets': assets,
        'allocations': allocations,
        'is_manager': is_mgr
    })


@login_required
def asset_manage(request, pk=None):
    if not is_hr_or_admin(request.user):
        return HttpResponseForbidden("Not authorized.")
        
    asset = get_object_or_404(Asset, pk=pk) if pk else None
    
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            messages.success(request, "Asset information updated.")
            return redirect('asset_list')
    else:
        form = AssetForm(instance=asset)
        
    return render(request, 'assets/asset_form.html', {
        'form': form,
        'title': 'Edit Asset Details' if pk else 'Register Asset'
    })


@login_required
def asset_allocate(request, pk=None):
    if not is_hr_or_admin(request.user):
        return HttpResponseForbidden("Not authorized.")
        
    allocation = get_object_or_404(AssetAllocation, pk=pk) if pk else None
    
    if request.method == 'POST':
        form = AssetAllocationForm(request.POST, instance=allocation)
        if form.is_valid():
            alloc = form.save()
            # Automatically update Asset status to Allocated if allocated and not returned yet
            asset = alloc.asset
            if alloc.returned_date:
                asset.status = 'Available'
            else:
                asset.status = 'Allocated'
            asset.save()
            
            messages.success(request, "Asset allocation saved.")
            return redirect('asset_list')
    else:
        form = AssetAllocationForm(instance=allocation)
        
    return render(request, 'assets/allocation_form.html', {
        'form': form,
        'title': 'Edit Allocation' if pk else 'Allocate Asset'
    })
