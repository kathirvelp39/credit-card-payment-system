from django.test import TestCase

# Create your tests here.

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from cards.models import Card
from transactions.models import Transaction


class TransactionManagementTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="transactionuser",
            password="TestPass123!",
        )
        self.other_user = User.objects.create_user(
            username="othertransactionuser",
            password="TestPass123!",
        )

        self.card = Card.objects.create(
            user=self.user,
            card_type="CREDIT",
            masked_card="************3456",
            last_four_digits="3456",
        )

        self.other_card = Card.objects.create(
            user=self.other_user,
            card_type="CREDIT",
            masked_card="************1111",
            last_four_digits="1111",
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.transaction = Transaction.objects.create(
            user=self.user,
            card=self.card,
            amount="2500.00",
            status="SUCCESS",
        )

        Transaction.objects.create(
            user=self.other_user,
            card=self.other_card,
            amount="5000.00",
            status="SUCCESS",
        )

    def test_user_sees_only_own_transactions(self):
        response = self.client.get("/api/transactions/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_filter_transactions_by_status(self):
        response = self.client.get(
            "/api/transactions/?status=SUCCESS"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["status"], "SUCCESS"
        )

    def test_unauthenticated_user_cannot_view_transactions(self):
        self.client.force_authenticate(user=None)

        response = self.client.get("/api/transactions/")

        self.assertEqual(response.status_code, 401)
