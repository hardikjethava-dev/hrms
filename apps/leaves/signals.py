from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LeaveRequest
from apps.notifications.models import Notification


@receiver(post_save, sender=LeaveRequest)
def leave_request_status_handler(sender, instance, created, **kwargs):
    if not created:
        if instance.status in ('Approved', 'Rejected'):
            try:
                Notification.objects.create(
                    recipient=instance.employee.user,
                    title=f"Leave Request {instance.status}",
                    message=f"Your leave request from {instance.start_date} to {instance.end_date} has been {instance.status}."
                )
            except Exception:
                pass
