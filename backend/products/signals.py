from django.db.models import Count
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Group, UserProductAccess


@receiver(post_save, sender=UserProductAccess)
def distribute_user_to_group(sender, instance, created, **kwargs):
    """
    Сигнал для добавления пользователя в группу
    при получении доступа к продукту.
    """
    if created:
        user = instance.user
        product = instance.product

        groups_with_counts = Group.objects.filter(
            product=product
        ).annotate(
            num_users=Count('students')
        )

        suitable_group = None
        for group in groups_with_counts:
            if group.num_users < product.max_users_in_group:
                suitable_group = group
                break

        if suitable_group is None:
            group_name = f'Группа №{groups_with_counts.count() + 1}'
            suitable_group = Group.objects.create(name=group_name,
                                                  product=product)

        suitable_group.students.add(user)


@receiver(post_delete, sender=UserProductAccess)
def remove_user_from_group(sender, instance, **kwargs):
    """
    Сигнал для удаления пользователя из группы
    при потере доступа к продукту.
    """
    user = instance.user
    product = instance.product

    groups = Group.objects.filter(product=product, students=user)

    for group in groups:
        group.students.remove(user)
