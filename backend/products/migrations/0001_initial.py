# Generated by Django 4.2.10 on 2024-02-29 07:05

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='название')),
                ('start_datetime', models.DateTimeField(verbose_name='дата старта')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='стоимость продукта')),
                ('min_users_in_group', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='минимальное кол-во студентов в группе')),
                ('max_users_in_group', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='максимальное кол-во студентов в группе')),
                ('number_of_groups', models.IntegerField(default=3, validators=[django.core.validators.MinValueValidator(1)], verbose_name='кол-во групп')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to=settings.AUTH_USER_MODEL, verbose_name='автор')),
            ],
            options={
                'verbose_name': 'продукт',
                'verbose_name_plural': 'продукты',
            },
        ),
        migrations.CreateModel(
            name='UserProductAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_accesses', to='products.product', verbose_name='продукт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_accesses', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'доступ к продукту',
                'verbose_name_plural': 'доступы к продуктам',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='название')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='продукт')),
                ('students', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='студенты')),
            ],
            options={
                'verbose_name': 'группа',
                'verbose_name_plural': 'группы',
            },
        ),
    ]