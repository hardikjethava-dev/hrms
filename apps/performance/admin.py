from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('employee', 'reviewer', 'review_period', 'rating', 'review_date')
    list_filter = ('rating', 'review_period')
    search_fields = ('employee__first_name', 'employee__last_name', 'feedback')
    ordering = ('-review_date',)
    readonly_fields = ('created_at', 'updated_at')
