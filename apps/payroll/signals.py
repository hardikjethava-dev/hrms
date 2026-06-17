from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payroll
from apps.notifications.models import Notification


@receiver(post_save, sender=Payroll)
def payroll_record_created_handler(sender, instance, created, **kwargs):
    if created:
        try:
            Notification.objects.create(
                recipient=instance.employee.user,
                title="Payslip Generated",
                message=f"Your payslip for {instance.get_month_display()} {instance.year} is now available."
            )
        except Exception:
            pass
