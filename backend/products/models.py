from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Product(models.Model):
    """
    Модель продукта.
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='автор'
    )
    name = models.CharField(
        max_length=255,
        verbose_name='название'
    )
    start_datetime = models.DateTimeField(
        verbose_name='дата старта'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='стоимость продукта'
    )
    min_users_in_group = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='минимальное кол-во студентов в группе'
    )
    max_users_in_group = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='максимальное кол-во студентов в группе'
    )

    def clean(self):
        if self.min_users_in_group > self.max_users_in_group:
            raise ValidationError(
                'Минимальное количество студентов в группе не может быть '
                'больше максимального.'
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'


class UserProductAccess(models.Model):
    """
    Модель доступа пользователя к продукту.
    """
    user = models.ForeignKey(
        User,
        related_name='product_accesses',
        on_delete=models.CASCADE,
        verbose_name='пользователь'
    )
    product = models.ForeignKey(
        Product,
        related_name='user_accesses',
        on_delete=models.CASCADE,
        verbose_name='продукт'
    )

    def __str__(self):
        return f'{self.user} имеет доступ к {self.product}'

    class Meta:
        verbose_name = 'доступ к продукту'
        verbose_name_plural = 'доступы к продуктам'


class Group(models.Model):
    """
    Модель группы.
    """
    name = models.CharField(max_length=255, verbose_name='название')
    students = models.ManyToManyField(User, verbose_name='студенты')
    product = models.ForeignKey(
        Product,
        related_name='groups',
        on_delete=models.CASCADE,
        verbose_name='продукт'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'группа'
        verbose_name_plural = 'группы'


class Lesson(models.Model):
    """
    Модель урока для продукта.
    """
    name = models.CharField(max_length=255, verbose_name='название')
    video_url = models.URLField(verbose_name='ссылка')
    product = models.ForeignKey(
        Product,
        related_name='lessons',
        on_delete=models.CASCADE,
        verbose_name='продукт'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
