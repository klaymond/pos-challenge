from rest_framework import serializers
from djmoney.contrib.django_rest_framework import MoneyField

from pos.models import Order, OrderProduct, CustomUser, Product

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']

# class CustomerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = ['name']

class ProductSerializer(serializers.ModelSerializer):
    """
    Creating a product serializer even though right now the only field is 'name'
    makes the code scalable in the long term. It also allows for overriding the 
    create method.
    """

    def create(self, validated_data):
        obj, created = Product.objects.get_or_create(**validated_data)
        return obj

    class Meta:
        model = Product
        fields = ['name']

class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer


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
