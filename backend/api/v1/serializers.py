from djoser.serializers import UserSerializer
from rest_framework import serializers

from products.models import Product, Group, UserProductAccess, Lesson


class ProductCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания/изменения продуктов.
    """
    author = UserSerializer(default=serializers.CurrentUserDefault())
    start_datetime = serializers.DateTimeField(
        format="%d-%m-%YT%H:%M:%S",
        input_formats=["%d-%m-%YT%H:%M"]
    )

    class Meta:
        model = Product
        fields = '__all__'

    def validate(self, data):
        if data['min_users_in_group'] > data['max_users_in_group']:
            raise serializers.ValidationError(
                {'detail': 'Минимальное количество студентов в группе не '
                           'может быть больше максимального.'}
            )
        return data


class GroupSerializer(serializers.ModelSerializer):
    """
    Сериализатор для групп.
    """

    class Meta:
        model = Group
        fields = '__all__'


class UserProductAccessSerializer(serializers.ModelSerializer):
    """
    Сериализатор для доступов к продуктам.
    """

    class Meta:
        model = UserProductAccess
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для уроков.
    """

    class Meta:
        model = Lesson
        fields = '__all__'


class ProductReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра продуктов.
    """
    author = UserSerializer()
    lessons_count = serializers.IntegerField()
    start_datetime = serializers.DateTimeField(format="%d-%m-%YT%H:%M:%S")

    class Meta:
        model = Product
        fields = ('id', 'author', 'name',
                  'start_datetime', 'price', 'lessons_count')
