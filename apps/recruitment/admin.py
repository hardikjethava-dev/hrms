from django.contrib import admin
from .models import JobOpening, Candidate

@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'experience_years', 'status')
    list_filter = ('status', 'department')
    search_fields = ('title', 'description', 'requirements')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'experience', 'status', 'job_opening')
    list_filter = ('status', 'job_opening')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
