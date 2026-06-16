from django import forms
from .models import SalaryStructure


class SalaryStructureForm(forms.ModelForm):
    class Meta:
        model = SalaryStructure
        fields = ['employee', 'basic_salary', 'hra', 'allowances', 'deductions', 'effective_date']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control', 'id': 'sal_employee'}),
            'basic_salary': forms.NumberInput(attrs={'class': 'form-control', 'id': 'sal_basic'}),
            'hra': forms.NumberInput(attrs={'class': 'form-control', 'id': 'sal_hra'}),
            'allowances': forms.NumberInput(attrs={'class': 'form-control', 'id': 'sal_allowance'}),
            'deductions': forms.NumberInput(attrs={'class': 'form-control', 'id': 'sal_deduction'}),
            'effective_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'sal_date'}),
        }
