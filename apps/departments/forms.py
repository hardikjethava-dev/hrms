from django import forms
from .models import Department


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'description', 'head']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'dept_name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'id': 'dept_code'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'id': 'dept_desc'}),
            'head': forms.Select(attrs={'class': 'form-control', 'id': 'dept_head'}),
        }
