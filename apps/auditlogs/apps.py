from django.apps import AppConfig


class AuditlogsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.auditlogs'

    def ready(self):
        from .signals import register_audit_signals
        register_audit_signals()
