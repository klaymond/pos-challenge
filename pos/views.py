from rest_framework import mixins, viewsets
from pos.base import CustomUser

from models import Customer, Product, Order, OrderProduct
import serializers

class UserViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    Users cannot be updated per requirements.
    """
    queryset = CustomUser.objects.all()
    serializer_class = serializers.UserSerializer

    def perform_destroy(self, instance):
        """
        This method overrides the destroy functionality to make user inactive 
        instead of deleting it.
        """
        instance.is_active = False

class OrderViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """
    Orders cannot be updated or deleted
    """
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
