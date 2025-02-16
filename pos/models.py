from django.db import models
from djmoney.models.fields import MoneyField

from parrot.base import BaseModel
        
class Customer(BaseModel):
    """
    This class represents a customer. For now customers don't have access to the
    API, therefore they are not considered users. If functionalities such as 
    online orders or loyalty systems are implemented then Customers should be 
    upgraded to users
    """

    name = models.CharField(max_length=75)

    def __str__(self):
        return self.name

class Product(BaseModel):
    """
    """

    name = models.CharField(max_length=200)   

    def __str__(self):
        return self.name 

class Order(BaseModel):
    """
    """

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, through="ProductInstance")

    def __str__(self):
        return f"Order number {self.pk} for {self.customer.name}"

class ProductInstance(BaseModel):
    """
    """
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='MXN')
