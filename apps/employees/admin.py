from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'first_name', 'last_name', 'email', 'employment_status', 'department', 'designation')
    list_filter = ('employment_type', 'employment_status', 'gender', 'department')
    search_fields = ('employee_id', 'first_name', 'last_name', 'email')
    ordering = ('employee_id',)
    readonly_fields = ('created_at', 'updated_at')
