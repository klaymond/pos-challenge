from django.db import models
from djmoney.models.fields import MoneyField
from django.db.models import Sum, F

from pos.base import BaseModel
        
# class Customer(BaseModel):
#     """
#     This class represents a customer. For now customers don't have access to the
#     API, therefore they are not considered users. If functionalities such as 
#     online orders or loyalty systems are implemented then Customers should be 
#     upgraded to users
#     """

#     name = models.CharField(max_length=75)

#     def __str__(self):
#         return self.name

class Product(BaseModel):
    """
    """

    name = models.CharField(max_length=200)   

    def __str__(self):
        return self.name 

class Order(BaseModel):
    """
    """

    customer_name = models.CharField(max_length=75)
    products = models.ManyToManyField(Product, through="OrderProduct")

    def __str__(self):
        return f"Order number {self.pk} for {self.customer.name}"
    
    @property
    def total(self):
        return self.products.aggregate(Sum(F("orderproduct__price") * F("orderproduct__quantity")))
    

class OrderProduct(BaseModel):
    """
    """
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='MXN')
    quantity = models.PositiveSmallIntegerField()
