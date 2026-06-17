from django.db import models
from apps.core.models import TimeStampedModel


class Holiday(TimeStampedModel):
    name = models.CharField(max_length=100)
    date = models.DateField(unique=True)
    description = models.TextField(blank=True)
    is_optional = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.date})"
