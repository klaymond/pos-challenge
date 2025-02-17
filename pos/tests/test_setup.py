import uuid
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from pos.models import *

class TestMyModelSetup(TestCase):

    def setUp(self):
        self.client = APIClient()
        fake_email = f"{str(uuid.uuid4())}@email.com"
        self.user1 = CustomUser.objects.create(
            email=fake_email,
        )
        fake_email = f"{str(uuid.uuid4())}@email.com"
        self.user2 = CustomUser.objects.create(
            email=fake_email,
        )
        refresh = RefreshToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')