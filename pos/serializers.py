from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from djmoney.contrib.django_rest_framework import MoneyField

from pos.models import Order, OrderProduct, CustomUser, Product

class ParrotMoneyField(MoneyField):
    
    def __init__(self, **kwargs):
        super().__init__(max_digits=10, decimal_places=2, **kwargs)

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

class OrderProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderProduct
        fields = ['price', 'quantity']

class ProductSerializer(serializers.ModelSerializer):
    """
    Creating a product serializer even though right now the only field is 'name'
    makes the code scalable in the long term. It also allows for overriding the 
    create method.
    """

    details = OrderProductSerializer(required=True, many=True)
    name = serializers.CharField(validators=[])

    class Meta:
        model = Product
        fields = ['name', 'details']

class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    total = ParrotMoneyField(read_only=True, required=False)

    def create(self, validated_data):
        order_product_data = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        for order_product in order_product_data:
            product, _ = Product.objects.get_or_create(name=order_product.pop('name'))
            OrderProduct.objects.create(order=order, product=product, **order_product.get('details')[0])
        return order

    def to_representation(self, instance):
        return {"customer_name": instance.customer_name, "total": instance.total}

    class Meta:
        model = Order
        fields = ['customer_name', 'products', 'total']

class ProductReportSerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=200)
    quantity_sold = serializers.IntegerField()
    total_price = ParrotMoneyField()

class ProductReportListSerializer(serializers.ListSerializer):
    products = ProductReportSerializer
