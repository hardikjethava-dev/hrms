from django.db import models
from apps.core.models import TimeStampedModel


class Review(TimeStampedModel):
    RATING_CHOICES = (
        (1, 'Poor'),
        (2, 'Fair'),
        (3, 'Good'),
        (4, 'Very Good'),
        (5, 'Excellent'),
    )

    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='performance_reviews'
    )
    reviewer = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='given_reviews'
    )
    review_period = models.CharField(max_length=50, help_text="e.g. Q1 2026, Annual 2025")
    rating = models.IntegerField(choices=RATING_CHOICES)
    feedback = models.TextField()
    review_date = models.DateField()

    def __str__(self):
        return f"Review for {self.employee} ({self.review_period}) by {self.reviewer}"
