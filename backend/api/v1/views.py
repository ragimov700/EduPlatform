from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from products.models import Product, UserProductAccess
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    @action(methods=['post'], detail=True)
    def purchase(self, request, pk):
        """
        Метод для покупки продукта пользователем.
        """
        user = self.request.user
        product = self.get_object()
        if UserProductAccess.objects.filter(user=user,
                                            product=product).exists():
            return Response(
                {'detail': 'Вы уже приобрели этот продукт.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user.balance < product.price:
            return Response(
                {'detail': 'На балансе недостаточно средств.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                user.balance -= product.price
                user.save()

                UserProductAccess.objects.create(user=user, product=product)

                product.author.balance += product.price
                product.author.save()
        except Exception as _:
            return Response(
                {'detail': 'Произошла ошибка, попробуйте позже.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {'detail': 'Вы успешно совершили покупку!'},
            status=status.HTTP_200_OK
        )
