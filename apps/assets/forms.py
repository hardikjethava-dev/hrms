from django import forms
from .models import Asset, AssetAllocation


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['asset_code', 'name', 'category', 'purchase_date', 'value', 'status']
        widgets = {
            'asset_code': forms.TextInput(attrs={'class': 'form-control', 'id': 'asset_code'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'asset_name'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'id': 'asset_cat'}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'asset_date'}),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'id': 'asset_val'}),
            'status': forms.Select(attrs={'class': 'form-control', 'id': 'asset_status'}),
        }


class AssetAllocationForm(forms.ModelForm):
    class Meta:
        model = AssetAllocation
        fields = ['asset', 'employee', 'allocated_date', 'returned_date']
        widgets = {
            'asset': forms.Select(attrs={'class': 'form-control', 'id': 'alloc_asset'}),
            'employee': forms.Select(attrs={'class': 'form-control', 'id': 'alloc_emp'}),
            'allocated_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'alloc_date'}),
            'returned_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'return_date'}),
        }
