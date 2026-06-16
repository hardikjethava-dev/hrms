from django.db import models
from apps.accounts.models import TimeStampedModel


class Shift(TimeStampedModel):
    name = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    grace_minutes = models.IntegerField(default=15)

    def __str__(self):
        return f"{self.name} ({self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')})"


class EmployeeShift(TimeStampedModel):
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='shifts'
    )
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    effective_from = models.DateField()

    def __str__(self):
        return f"{self.employee} - {self.shift} from {self.effective_from}"
