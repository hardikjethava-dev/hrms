from django.db import models
from apps.accounts.models import TimeStampedModel


class JobPosition(TimeStampedModel):
    STATUS_CHOICES = (
        ('Draft', 'Draft'),
        ('Open', 'Open'),
        ('Closed', 'Closed'),
    )

    title = models.CharField(max_length=100)
    department = models.ForeignKey(
        'departments.Department',
        on_delete=models.CASCADE,
        related_name='job_positions'
    )
    description = models.TextField()
    vacancies = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft')

    def __str__(self):
        return f"{self.title} - {self.department.name} ({self.status})"


class Candidate(TimeStampedModel):
    STATUS_CHOICES = (
        ('Applied', 'Applied'),
        ('Screening', 'Screening'),
        ('Interview', 'Interview'),
        ('Selected', 'Selected'),
        ('Rejected', 'Rejected'),
        ('Hired', 'Hired'),
    )

    job_position = models.ForeignKey(
        JobPosition,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='candidates'
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    resume = models.FileField(upload_to='resumes/')
    experience = models.DecimalField(max_digits=4, decimal_places=1, help_text="Experience in years")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Applied')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.job_position.title if self.job_position else 'General'}"
