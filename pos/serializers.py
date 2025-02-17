from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from djmoney.contrib.django_rest_framework import MoneyField

from pos.models import Order, OrderProduct, CustomUser, Product

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

# class CustomerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = ['name']



# class CreatableSlugRelatedField(serializers.SlugRelatedField):
#     """
#     This field allows for the name to be used as a SlugRelatedField for the
#     product so it can be created in the same call as the order.
#     """
#     def to_internal_value(self, data):
#         try:
#             return self.get_queryset().get(**{self.slug_field: data})
#         except ObjectDoesNotExist:
#             return self.get_queryset().create(**{self.slug_field: data})
#         except (TypeError, ValueError):
#             self.fail('invalid')

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

    # def create(self, validated_data):
    #     print('hola')
    #     print(validated_data)
    #     obj, created = Product.objects.get_or_create(**validated_data)
    #     return obj

    class Meta:
        model = Product
        fields = ['name', 'details']

class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    total = MoneyField(max_digits=10, decimal_places=2, read_only=True, required=False)

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

class ProductReportSerializer(serializers.ListSerializer):
    pass
