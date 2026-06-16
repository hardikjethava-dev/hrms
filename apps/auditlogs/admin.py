from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action', 'model_name', 'object_id', 'ip_address')
    list_filter = ('action', 'model_name', 'timestamp')
    search_fields = ('model_name', 'object_id', 'user__email')
    readonly_fields = ('user', 'action', 'model_name', 'object_id', 'timestamp', 'ip_address')
