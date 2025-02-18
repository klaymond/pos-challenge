import uuid

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from pos.models import *
from .data import *

class IntegrationTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.fake_email = f"{str(uuid.uuid4())}@email.com"
        self.user1 = CustomUser.objects.create(
            email=self.fake_email,
            username='user1'
        )
        refresh = RefreshToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
    
    def test_crud_user(self):
        response = self.client.post('/users/', USER_PAYLOAD, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get('/users/2/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.patch('/users/1/', {"email": "jorge@parrot.com"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.delete('/users/2/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_crud_order(self):
        for i, order in enumerate(ORDER_PAYLOADS):
            response = self.client.post('/orders/', order, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(f'/orders/{2}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.patch('/orders/3/', {"customer": "Jorge"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.delete('/orders/3/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_list_product_report(self):
        response = self.client.get('/report/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    