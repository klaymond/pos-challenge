from django.db.models import Sum, F
from rest_framework import mixins, viewsets, generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from pos.models import Order, CustomUser, OrderProduct
from pos import serializers

class UserViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    Users cannot be updated per requirements.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer

class SalesReportView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ProductReportSerializer
    queryset = OrderProduct.objects.all()

    def get_queryset(self):
        """
        Filter from query parameters. And aggregate data
        """
        queryset = OrderProduct.objects.all()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        queryset = queryset.filter(order__creation_date__range=[start_date, end_date])
        queryset = queryset.values('product').annotate(
            quantity_sold=Sum("quantity"),
            total_price=Sum(
                F("price") * F("quantity")
                ),
            product_name=F('product__name' )
            ).order_by("-quantity_sold")
        return queryset
