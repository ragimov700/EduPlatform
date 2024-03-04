from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from products.models import Product, UserProductAccess
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import (
    ProductCreateSerializer,
    LessonSerializer,
    ProductReadSerializer
)

User = get_user_model()


class ProductViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для продуктов.
    """
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ProductReadSerializer
        return ProductCreateSerializer

    def get_queryset(self):
        if self.action == 'list' or self.action == 'retrieve':
            return Product.objects.annotate(
                lessons_count=Count('lessons')
            ).select_related(
                'author'
            ).all()
        return Product.objects.all()

    @action(methods=['post'], detail=True)
    def purchase(self, request, pk):
        """
        Метод для покупки продукта пользователем.
        """
        user = self.request.user
        product = self.get_object()

        if product.user_accesses.filter(user=user).exists():
            return Response(
                {'detail': 'Вы уже приобрели этот продукт.'},
                status=status.HTTP_403_FORBIDDEN
            )

        if user.balance < product.price:
            return Response(
                {'detail': 'На балансе недостаточно средств.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                user.balance -= product.price
                author = product.author
                author.balance += product.price

                User.objects.bulk_update([user, author], ['balance'])

                UserProductAccess.objects.create(user=user, product=product)
        except Exception as _:
            return Response(
                {'detail': 'Произошла ошибка, попробуйте позже.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {'detail': 'Вы успешно совершили покупку!'},
            status=status.HTTP_200_OK
        )

    @action(methods=['get'], detail=True)
    def lessons(self, request, pk):
        """
        Метод для просмотра уроков продукта.
        """
        user = self.request.user
        product = self.get_object()

        if not product.user_accesses.filter(user=user).exists():
            return Response(
                {'detail': 'У вас нет доступа к этому продукту.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = LessonSerializer(product.lessons, many=True)
        return Response(serializer.data)
