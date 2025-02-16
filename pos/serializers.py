from rest_framework import serializers

from models import Customer, Product, Order, ProductInstance
from parrot.base import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['customer', 'products']
        depth = 1

class ProductInstanceSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField

    class Meta:
        model = ProductInstance
        fields = ['product', 'price']

class ProductReportSerializer(serializers.ListSerializer):
    pass
