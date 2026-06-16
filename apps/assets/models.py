from django.db import models
from apps.accounts.models import TimeStampedModel


class Asset(TimeStampedModel):
    STATUS_CHOICES = (
        ('Available', 'Available'),
        ('Allocated', 'Allocated'),
        ('Maintenance', 'Maintenance'),
        ('Scrapped', 'Scrapped'),
    )

    asset_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    purchase_date = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')

    def __str__(self):
        return f"{self.name} ({self.asset_code}) - {self.status}"


class AssetAllocation(TimeStampedModel):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='allocations')
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='allocated_assets'
    )
    allocated_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.asset.name} allocated to {self.employee} on {self.allocated_date}"
