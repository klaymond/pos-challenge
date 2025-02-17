from django.db import models
from djmoney.models.fields import MoneyField
from django.db.models import Sum, F
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    This should be used instead of the built-in User from Django. This is 
    because of a requirement for users to have email as a unique identifier.
    """
    email = models.EmailField(unique=True)

class BaseModel(models.Model):
    """
    Base model that allows for additional tracking of creation and update of 
    models.
    All application models should inherit from this abstract model instead of 
    models.Model.
    """

    creation_date = models.DateTimeField(
        auto_now_add=True, editable=False, null=True, verbose_name='Creation Date')
    last_update_date = models.DateTimeField(
        auto_now=True, editable=False, null=True, verbose_name='Last Update Date')

    created_by = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, null=True, related_name="+",
        editable=False, db_column="created_by", default=1,
    )
    last_updated_by = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, null=True, related_name="+",
        editable=False, db_column="last_updated_by", default=1
    )

    class Meta:
        abstract = True

    def created_by_name(self):
        if self.created_by:
            return self.created_by.get_full_name().strip() or self.created_by.username

    def last_updated_by_name(self):
        if self.last_updated_by:
            return self.last_updated_by.get_full_name().strip() or self.last_updated_by.username

class Product(BaseModel):
    """
    Product only has a name for now. An order can contain multiple products and
    in that order relationship price and quantities are defined.
    """

    name = models.CharField(max_length=200, unique=True)   

    def __str__(self):
        return self.name 

class Order(BaseModel):
    """
    An order is assigned to a customer who is only a charfield for now. It
    relates to Product in a many-to-many relationship. Each order can have one
    customer and multiple products with arbitrary prices. There can be an 
    arbitrary amount of said product with a certain price in an order. There can
    also be multiple prices for a single product in an order.
    """

    customer_name = models.CharField(max_length=75)
    products = models.ManyToManyField(Product, through="OrderProduct", related_name='details')

    def __str__(self):
        return f"Order number {self.pk} for {self.customer_name}"
    
    @property
    def total(self):
        return self.products.aggregate(
                total=Sum(
                    F("orderproduct__price") * F("orderproduct__quantity")
                    )
            ).get("total")
    

class OrderProduct(BaseModel):
    """
    Intermediate table that houses relationship between orders and products.
    This is needed because of the added information in terms of price and 
    quantity.
    """

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='MXN')
    quantity = models.PositiveSmallIntegerField()
