from django.contrib import admin
from .models import EmployeeDocument

@admin.register(EmployeeDocument)
class EmployeeDocumentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'document_type', 'created_at', 'expiry_date')
    list_filter = ('document_type',)
    search_fields = ('employee__first_name', 'employee__last_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
