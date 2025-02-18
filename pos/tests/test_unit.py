import decimal

from django.test import TestCase
from pos.models import Order, OrderProduct, Product, CustomUser


class ModelTest(TestCase):
    """ 
    Test module for all models, serializers and views. In a long term code base 
    there should be a TestCase for each model, serializer and view.
    """

    def setUp(self):
        user = CustomUser.objects.create(username='Aldo')
        product1 = Product.objects.create(
            name='Coca Cola', created_by=user, last_updated_by=user)
        product2 = Product.objects.create(
            name='Jocho', created_by=user, last_updated_by=user)
        order1 = Order.objects.create(
            customer_name='Uri', created_by=user, last_updated_by=user)
        order2 = Order.objects.create(
            customer_name='Gustavo', created_by=user, last_updated_by=user)
        OrderProduct.objects.create(
            order=order1, product=product1, quantity=2, price=12.34, 
            created_by=user, last_updated_by=user)
        OrderProduct.objects.create(
            order=order1, product=product2, quantity=4, price=92.33, 
            created_by=user, last_updated_by=user)
        OrderProduct.objects.create(
            order=order2, product=product1, quantity=8, price=95.33, 
            created_by=user, last_updated_by=user)
        OrderProduct.objects.create(
            order=order2, product=product2, quantity=6, price=45.2, 
            created_by=user, last_updated_by=user)

    def test_order_total(self):
        order1 = Order.objects.get(customer_name='Uri')
        order2 = Order.objects.get(customer_name='Gustavo')
        self.assertEqual(
            order1.total, 394.00)
        self.assertEqual(
            order2.total, decimal.Decimal('1033.84'))
