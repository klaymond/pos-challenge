from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from djmoney.contrib.django_rest_framework import MoneyField

from pos.models import Order, OrderProduct, CustomUser, Product

class ParrotMoneyField(MoneyField):
    """
    This extends MoneyField to keep all money values consistent accross 
    serializers.
    """
    
    def __init__(self, **kwargs):
        super().__init__(max_digits=10, decimal_places=2, **kwargs)

class UserSerializer(serializers.ModelSerializer):
    """
    User serializer.
    """

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
    """
    Serializer for many-to-many relationship between orders and products. This
    allows for price and quantity to be set for each product in the order.
    """

    class Meta:
        model = OrderProduct
        fields = ['price', 'quantity']

class ProductSerializer(serializers.ModelSerializer):
    """
    Product serializer that allows for multiple prices and quantities to be 
    set for the same product in one go.
    """

    details = OrderProductSerializer(required=True, many=True)
    name = serializers.CharField(validators=[])

    class Meta:
        model = Product
        fields = ['name', 'details']

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer ofr the order. This is the main point where the sales 
    functionalities interact with each other.
    """

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
        result = {}
        result["customer_name"] = instance.customer_name
        result["total"] = instance.total
        result["products"] = []
        for product in instance.orderproduct_set.all():
            product_representation = {
                "name": product.product.name,
                "quantity": product.quantity,
                "price": str(product.price),
            }
            result["products"].append(product_representation)
        return result

    class Meta:
        model = Order
        fields = ['customer_name', 'products', 'total']

class ProductReportSerializer(serializers.Serializer):
    """
    Serializer that flattens a product so that it only has one quantity and one 
    total price. Used for reporting purposes
    """

    product_name = serializers.CharField(max_length=200)
    quantity_sold = serializers.IntegerField()
    total_price = ParrotMoneyField()

class ProductReportListSerializer(serializers.ListSerializer):
    """
    List serializer that houses multiple flattened products. Used for reporting 
    purposes.
    """
    
    products = ProductReportSerializer
