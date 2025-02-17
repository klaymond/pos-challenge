from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_str
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

# class ProductSerializer(serializers.ModelSerializer):
#     """
#     Creating a product serializer even though right now the only field is 'name'
#     makes the code scalable in the long term. It also allows for overriding the 
#     create method.
#     """

#     def create(self, validated_data):
#         obj, created = Product.objects.get_or_create(**validated_data)
#         return obj

#     class Meta:
#         model = Product
#         fields = ['name']

class CreatableSlugRelatedField(serializers.SlugRelatedField):
    """
    This field allows for the name to be used as a SlugRelatedField for the
    product so it can be created in the same call as the order.
    """
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get_or_create(**{self.slug_field: data})[0]
        except ObjectDoesNotExist:
            self.fail('does_not_exist', slug_name=self.slug_field, value=smart_str(data))
        except (TypeError, ValueError):
            self.fail('invalid')

class OrderProductSerializer(serializers.ModelSerializer):
    product = CreatableSlugRelatedField(
        slug_field='name',
        queryset=Product.objects.all(),
    )

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
