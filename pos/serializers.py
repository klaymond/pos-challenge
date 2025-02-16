from rest_framework import serializers
from djmoney.contrib.django_rest_framework import MoneyField

from pos.models import Order, OrderProduct, CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']

# class CustomerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = ['name']

# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['name']

class OrderProductSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField


    class Meta:
        model = OrderProduct
        fields = ['product', 'price', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True)
    total = MoneyField(max_digits=10, decimal_places=2, read_only=True, required=False)

    class Meta:
        model = Order
        fields = ['customer_name', 'products', 'total']

class ProductReportSerializer(serializers.ListSerializer):
    pass
