from django.test import TestCase

# Create your tests here.

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from cards.models import Card


class CardManagementTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="carduser",
            password="TestPass123!",
        )
        self.other_user = User.objects.create_user(
            username="otheruser",
            password="TestPass123!",
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_add_card_stores_only_masked_number(self):
        response = self.client.post(
            "/api/cards/",
            {
                "card_type": "CREDIT",
                "card_number": "1234567890123456",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        card = Card.objects.get(user=self.user)
        self.assertEqual(card.last_four_digits, "3456")
        self.assertEqual(card.masked_card, "************3456")
        self.assertFalse(hasattr(card, "card_number"))

    def test_user_can_only_see_own_cards(self):
        Card.objects.create(
            user=self.other_user,
            card_type="CREDIT",
            masked_card="************1111",
            last_four_digits="1111",
        )

        response = self.client.get("/api/cards/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_unauthenticated_user_cannot_view_cards(self):
        self.client.force_authenticate(user=None)

        response = self.client.get("/api/cards/")

        self.assertEqual(response.status_code, 401)

