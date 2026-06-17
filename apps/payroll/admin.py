from django.contrib import admin
from .models import SalaryStructure, Payroll

@admin.register(SalaryStructure)
class SalaryStructureAdmin(admin.ModelAdmin):
    list_display = ('employee', 'base_salary', 'hra', 'allowances', 'deductions', 'effective_date')
    search_fields = ('employee__first_name', 'employee__last_name')
    ordering = ('employee',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('employee', 'month', 'year', 'gross_salary', 'total_deductions', 'net_salary')
    list_filter = ('month', 'year')
    search_fields = ('employee__first_name', 'employee__last_name')
    ordering = ('-year', '-month', 'employee')
    readonly_fields = ('created_at', 'updated_at')
