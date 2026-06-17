from django.db import models
from apps.core.models import TimeStampedModel


class EmployeeDocument(TimeStampedModel):
    DOCUMENT_TYPE_CHOICES = (
        ('Resume', 'Resume'),
        ('Offer Letter', 'Offer Letter'),
        ('Contract', 'Contract'),
        ('Certificate', 'Certificate'),
        ('Government ID', 'Government ID'),
        ('Other', 'Other'),
    )

    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='documents'
    )
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES)
    file = models.FileField(upload_to='employee_docs/')
    expiry_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.document_type} for {self.employee}"
