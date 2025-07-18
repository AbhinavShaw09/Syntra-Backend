from model_bakery import baker
from rest_framework import status
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
        self.product1 = self.make_model("Product", inventory_count=10)
        self.buyer_address = self.make_model("BuyerAddress", user=self.user)

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

    def get_buyer_cart_payload(self):
        return [{"product_id": str(self.product1.id), "quantity": 5}]

    def create_buyer_cart(self):
        return self.client.post(
            "/api/buyer/cart/",
            data=self.get_buyer_cart_payload(),
            content_type="application/json",
        )

    def assertSuccessReponse(self, response):
        allowed_statuses = [
            status.HTTP_200_OK,
            status.HTTP_201_CREATED,
            status.HTTP_202_ACCEPTED,
            status.HTTP_204_NO_CONTENT,
        ]

        assert response.status_code in allowed_statuses, (
            f"Expected success response, got {response.status_code}:\n{response.data}"
        )

    def assertErrorResponse(self, response):
        allowed_statuses = [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

        assert response.status_code in allowed_statuses, (
            f"Expected error response, got {response.status_code}:\n{response.data}"
        )

    def assertNoDataInReponse(self, response):
        self.assertEqual(len(response.data), 0)
