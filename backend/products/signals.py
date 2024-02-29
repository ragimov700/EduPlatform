from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, Group


@receiver(post_save, sender=Product)
def create_product_groups(sender, instance, created, **kwargs):
    """
    Сигнал для создания групп продукта.
    """
    if created:
        for i in range(instance.number_of_groups):
            Group.objects.create(product=instance, name=f'Группа №{i + 1}')
