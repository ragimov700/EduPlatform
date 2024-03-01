from rest_framework import permissions


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    """
    Предоставляет разрешение на чтение для авторизованных пользователей,
    но ограничивает доступ к изменению и удалению объектов только их авторам
    или если пользователь имеет статус персонала (is_staff).
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or request.user.is_staff)
