from django.contrib import admin
from .models import JobPosition, Candidate

@admin.register(JobPosition)
class JobPositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'vacancies', 'status')
    list_filter = ('status', 'department')
    search_fields = ('title',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'experience', 'status')
    list_filter = ('status',)
    search_fields = ('first_name', 'last_name', 'email')
    readonly_fields = ('created_at', 'updated_at')
