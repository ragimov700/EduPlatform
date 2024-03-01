from rest_framework import serializers

from products.models import Product, Group, UserProductAccess, Lesson


class ProductSerializer(serializers.ModelSerializer):
    author = serializers.CurrentUserDefault()

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
    class Meta:
        model = Group
        fields = '__all__'


class UserProductAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProductAccess
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
