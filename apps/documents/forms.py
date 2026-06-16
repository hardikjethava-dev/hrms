from django import forms
from .models import EmployeeDocument


class EmployeeDocumentForm(forms.ModelForm):
    class Meta:
        model = EmployeeDocument
        fields = ['employee', 'document_type', 'file', 'expiry_date']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control', 'id': 'doc_employee'}),
            'document_type': forms.Select(attrs={'class': 'form-control', 'id': 'doc_type'}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'id': 'doc_file'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'doc_expiry'}),
        }
