from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Employee
from apps.notifications.models import Notification


@receiver(post_save, sender=Employee)
def employee_created_handler(sender, instance, created, **kwargs):
    if created:
        try:
            Notification.objects.create(
                recipient=instance.user,
                title="Welcome to HRMS!",
                message=f"Hello {instance.first_name}, your employee profile has been created successfully. Feel free to explore the portal."
            )
        except Exception:
            pass
