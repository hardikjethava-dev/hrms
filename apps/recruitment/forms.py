from django import forms
from .models import JobPosition, Candidate


class JobPositionForm(forms.ModelForm):
    class Meta:
        model = JobPosition
        fields = ['title', 'department', 'description', 'vacancies', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'id': 'job_title'}),
            'department': forms.Select(attrs={'class': 'form-control', 'id': 'job_dept'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'id': 'job_desc'}),
            'vacancies': forms.NumberInput(attrs={'class': 'form-control', 'id': 'job_vacancies'}),
            'status': forms.Select(attrs={'class': 'form-control', 'id': 'job_status'}),
        }


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['job_position', 'first_name', 'last_name', 'email', 'phone', 'resume', 'experience', 'status']
        widgets = {
            'job_position': forms.Select(attrs={'class': 'form-control', 'id': 'cand_job'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'cand_first_name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'cand_last_name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'cand_email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'id': 'cand_phone'}),
            'resume': forms.FileInput(attrs={'class': 'form-control', 'id': 'cand_resume'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'id': 'cand_exp'}),
            'status': forms.Select(attrs={'class': 'form-control', 'id': 'cand_status'}),
        }
