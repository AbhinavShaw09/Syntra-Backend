from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "securepass123"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = APIClient()
        self.auth_client = self.get_auth_client(self.user)

    def get_access_token(self, user=None):
        user = user or self.user
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def get_auth_client(self, user=None):
        token = self.get_access_token(user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        return client
