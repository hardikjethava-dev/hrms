from django.db import models
from django.conf import settings
from apps.accounts.models import TimeStampedModel


class Employee(TimeStampedModel):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    
    EMPLOYMENT_TYPE_CHOICES = (
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Contract', 'Contract'),
        ('Intern', 'Intern'),
    )
    
    EMPLOYMENT_STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Probation', 'Probation'),
        ('Notice Period', 'Notice Period'),
        ('Resigned', 'Resigned'),
        ('Terminated', 'Terminated'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='employee_profile'
    )
    employee_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    joining_date = models.DateField()
    employment_type = models.CharField(max_length=30, choices=EMPLOYMENT_TYPE_CHOICES, default='Full Time')
    employment_status = models.CharField(max_length=30, choices=EMPLOYMENT_STATUS_CHOICES, default='Active')
    designation = models.CharField(max_length=100)
    department = models.ForeignKey(
        'departments.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees'
    )
    manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordinates'
    )
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_id})"
