from django.db.models import Sum, F
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
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
    queryset = Order.objects.all().prefetch_related()
    serializer_class = serializers.OrderSerializer

class SalesReportView(generics.ListAPIView):
    """
    Simple list view that returns a report detailing product earnings and 
    quantities sold. This report is cached for 2 hours since there is no use for
    real time data. Ideally this view gets cached with new values after closing
    the restaurant cash register.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ProductReportSerializer
    queryset = OrderProduct.objects.all().prefetch_related()

    # Cache page for the requested url
    @method_decorator(cache_page(60*60*2))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def get_queryset(self):
        """
        Filter from query parameters and aggregate data for report.
        """
        queryset = self.queryset
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
