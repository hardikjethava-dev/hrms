from django.db import models
from apps.core.models import TimeStampedModel


class LeaveType(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)
    days_per_year = models.IntegerField(default=15)
    is_paid = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.days_per_year} days/yr)"


class LeaveBalance(TimeStampedModel):
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='leave_balances'
    )
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    allowed_days = models.IntegerField(default=15)
    remaining_days = models.IntegerField(default=15)

    class Meta:
        unique_together = ('employee', 'leave_type')

    def __str__(self):
        return f"{self.employee} - {self.leave_type.name}: {self.remaining_days}/{self.allowed_days} days left"


class LeaveRequest(TimeStampedModel):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Cancelled', 'Cancelled'),
    )

    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='leave_requests'
    )
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    approved_by = models.ForeignKey(
        'employees.Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_leaves'
    )
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee} - {self.leave_type.name} ({self.start_date} to {self.end_date}): {self.status}"
