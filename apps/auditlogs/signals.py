from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import AuditLog
from .middleware import get_current_user


def log_action(sender, instance, action_name, created=None):
    user = get_current_user()
    model_name = sender.__name__
    object_id = str(instance.pk)
    
    if model_name == 'AuditLog':
        return
        
    action = action_name
    if action_name == 'Save':
        action = 'Create' if created else 'Update'
        
    try:
        AuditLog.objects.create(
            user=user,
            action=action,
            model_name=model_name,
            object_id=object_id
        )
    except Exception:
        pass


def make_save_handler(model_class):
    def save_handler(sender, instance, created, **kwargs):
        log_action(sender, instance, 'Save', created)
    return save_handler


def make_delete_handler(model_class):
    def delete_handler(sender, instance, **kwargs):
        log_action(sender, instance, 'Delete')
    return delete_handler


def register_audit_signals():
    # Local imports to avoid circular imports during setup
    from apps.employees.models import Employee
    from apps.departments.models import Department
    from apps.leaves.models import LeaveRequest
    from apps.payroll.models import Payroll, SalaryStructure
    from apps.assets.models import Asset
    from apps.documents.models import EmployeeDocument
    from apps.attendance.models import Attendance
    
    User = get_user_model()
    tracked_models = [User, Employee, Department, LeaveRequest, Payroll, SalaryStructure, Asset, EmployeeDocument, Attendance]

    for model in tracked_models:
        post_save.connect(make_save_handler(model), sender=model, dispatch_uid=f"audit_save_{model.__name__}")
        post_delete.connect(make_delete_handler(model), sender=model, dispatch_uid=f"audit_delete_{model.__name__}")
