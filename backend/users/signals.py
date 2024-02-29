from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def set_initial_balance(sender, instance, created, **kwargs):
    """
    Сигнал для зачисления стартового баланса пользователю.
    """
    if created:
        instance.balance = 50.00
        instance.save()
