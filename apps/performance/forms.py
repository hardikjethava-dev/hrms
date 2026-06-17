from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['employee', 'reviewer', 'review_period', 'rating', 'feedback', 'review_date']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control', 'id': 'review_employee'}),
            'reviewer': forms.Select(attrs={'class': 'form-control', 'id': 'review_reviewer'}),
            'review_period': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Q2 2026', 'id': 'review_period'}),
            'rating': forms.Select(attrs={'class': 'form-control', 'id': 'review_rating'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'id': 'review_feedback'}),
            'review_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'review_date'}),
        }
