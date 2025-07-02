from model_bakery import baker
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from api.models import Buyer
from api.utils.test_utils import (
    generate_random_username,
    generate_random_email,
    generate_random_password,
)


class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.username = generate_random_username()
        self.email = generate_random_email()
        self.password = generate_random_password()
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )
        self.buyer = Buyer.objects.get_or_create(
            user_id=self.user.id, email=self.user.email
        )[0]
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

    def make_model(self, instance, **kwargs):
        return baker.make(instance, **kwargs)
