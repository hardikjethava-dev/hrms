from django.contrib import admin
from .models import PerformanceReview

@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ('employee', 'reviewer', 'review_period', 'rating', 'review_date')
    list_filter = ('rating', 'review_period')
    search_fields = ('employee__first_name', 'employee__last_name')
    readonly_fields = ('created_at', 'updated_at')
