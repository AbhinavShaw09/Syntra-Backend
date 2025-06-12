from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

from api.tests.base import BaseAPITestCase


class AuthIntegrationTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.register_url = "/api/auth/register/"
        self.login_url = "/api/auth/login/"

    def test_user_registration(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword123",
        }
        resp = self.client.post(
            self.register_url,
            data=data,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", resp.data)

    def test_login_success(self):
        data = {"username": self.username, "password": self.password}
        resp = self.client.post(
            self.login_url,
            data=data,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", resp.data)
              
    def test_login_invalid_credentials(self):
        data = {"username": self.username, "password": "wrongpassword"}
        resp = self.client.post(
            self.login_url,
            data=data,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
