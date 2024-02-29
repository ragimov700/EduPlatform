from products.models import Product, Group, UserProductAccess
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class UserProductAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProductAccess
        fields = '__all__'
