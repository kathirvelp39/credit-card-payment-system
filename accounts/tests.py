from django.test import TestCase

# Create your tests here.

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = "/api/accounts/register/"
        self.profile_url = "/api/accounts/profile/"

    def test_user_registration(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPass123!",
        }

        response = self.client.post(
            self.register_url, data, format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            User.objects.filter(username="testuser").exists()
        )

    def test_profile_requires_authentication(self):
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, 401)

    def test_login_with_correct_password(self):
        User.objects.create_user(
            username="loginuser",
            password="TestPass123!",
        )

        response = self.client.post(
            "/api/token/",
            {
                "username": "loginuser",
                "password": "TestPass123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
