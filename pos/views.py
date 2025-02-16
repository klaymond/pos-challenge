from rest_framework import mixins, viewsets
from parrot.base import CustomUser

from models import Customer, Product, Order, ProductInstance
import serializers

class UserViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.DestroyModelMixin,
                                viewsets.GenericViewSet):
    """
    """
    queryset = CustomUser.objects.all()
    serializer_class = serializers.UserSerializer

    def perform_destroy(self, instance):
        """
        This method overrides the destroy functionality to make user inactive 
        instead of deleting it.
        """
        instance.is_active = False
