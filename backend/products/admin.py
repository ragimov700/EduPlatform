from django.contrib import admin
from .models import Product, Group, UserProductAccess, Lesson


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Конфигурация админки для модели продукта.
    """
    list_display = ['name', 'start_datetime', 'price']
    list_filter = ['start_datetime']
    search_fields = ['name']


@admin.register(UserProductAccess)
class UserProductAccessAdmin(admin.ModelAdmin):
    """
    Конфигурация админки для модели доступа к продукту.
    """
    list_display = ['user', 'product']
    list_filter = ['product']
    search_fields = ['user__username', 'product__name']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """
    Конфигурация админки для модели группы.
    """
    list_display = ['name', 'product']
    list_filter = ['product']
    search_fields = ['name']
    filter_horizontal = ['students']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """
    Конфигурация админки для уроков продукта.
    """
    list_display = ['name', 'product']
    search_fields = ['name']
