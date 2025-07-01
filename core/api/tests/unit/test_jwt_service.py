from ..base import BaseAPITestCase
from django.contrib.auth.models import User

from api.services import JwtService
from api.models import Seller, Buyer


class JwtServiceTests(BaseAPITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="securepass",
        )
        self.user.name = "Test User"
        self.user.email = "test@example.com"
        self.user.save()

    def test_token_creation_creates_seller_and_buyer(self):
        service = JwtService(self.user)
        token = service.get_token()

        self.assertIn("name", token)
        self.assertIn("phone", token)
        self.assertIn("seller_id", token)
        self.assertIn("buyer_id", token)

        self.assertTrue(Seller.objects.filter(user=self.user).exists())
        self.assertTrue(Buyer.objects.filter(user=self.user).exists())

    def test_token_fields_match_user(self):
        service = JwtService(self.user)
        token = service.get_token()

        self.assertEqual(token["name"], self.user.username)

    def test_raises_error_for_invalid_user(self):
        service = JwtService(self.user)
        User.objects.filter(id=self.user.id).delete()

        with self.assertRaises(ValueError):
            service.get_token()
