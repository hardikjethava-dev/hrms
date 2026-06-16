from django.contrib import admin
from .models import Shift, EmployeeShift

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time', 'grace_minutes')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(EmployeeShift)
class EmployeeShiftAdmin(admin.ModelAdmin):
    list_display = ('employee', 'shift', 'effective_from')
    readonly_fields = ('created_at', 'updated_at')
