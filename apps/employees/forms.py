from django import forms
from .models import Employee
from django.contrib.auth import get_user_model

User = get_user_model()

class EmployeeForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'emp_email'}))
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'id': 'emp_role'}))
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Optional/Set password for new accounts', 'id': 'emp_password'})
    )

    class Meta:
        model = Employee
        fields = [
            'employee_id', 'first_name', 'last_name', 'phone', 
            'date_of_birth', 'gender', 'joining_date', 
            'employment_type', 'employment_status', 'designation', 
            'department', 'manager', 'address', 'profile_picture'
        ]
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control', 'id': 'emp_id'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'emp_first_name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'emp_last_name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'id': 'emp_phone'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'emp_dob'}),
            'gender': forms.Select(attrs={'class': 'form-control', 'id': 'emp_gender'}),
            'joining_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'emp_join_date'}),
            'employment_type': forms.Select(attrs={'class': 'form-control', 'id': 'emp_type'}),
            'employment_status': forms.Select(attrs={'class': 'form-control', 'id': 'emp_status'}),
            'designation': forms.TextInput(attrs={'class': 'form-control', 'id': 'emp_designation'}),
            'department': forms.Select(attrs={'class': 'form-control', 'id': 'emp_department'}),
            'manager': forms.Select(attrs={'class': 'form-control', 'id': 'emp_manager'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'id': 'emp_address'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control', 'id': 'emp_pic'}),
        }
