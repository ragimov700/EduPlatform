from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Конфигурация админки для модели пользователя.
    """
    list_display = ('username', 'email', 'balance')
    search_fields = ('username', 'email')
