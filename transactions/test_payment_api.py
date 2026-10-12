
from django.contrib.auth.models import User
from django.test import TestCase

from cards.models import Card
from transactions.models import Transaction
from decimal import Decimal


class PaymentProcessingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="paymentuser",
            password="TestPass123!",
        )

        self.card = Card.objects.create(
            user=self.user,
            card_type="CREDIT",
            masked_card="************3456",
            last_four_digits="3456",
        )

    def test_successful_payment_record(self):
        transaction = Transaction.objects.create(
            user=self.user,
            card=self.card,
            amount="2500.00",
            status="SUCCESS",
        )

        self.assertEqual(transaction.status, "SUCCESS")
        self.assertEqual(Decimal(str(transaction.amount)), Decimal("2500.00"))

    def test_failed_payment_record(self):
        transaction = Transaction.objects.create(
            user=self.user,
            card=self.card,
            amount="15000.00",
            status="FAILED",
        )

        self.assertEqual(transaction.status, "FAILED")
        self.assertEqual(Decimal(str(transaction.amount)), Decimal("15000.00"))

    def test_payment_defaults_to_pending(self):
        transaction = Transaction.objects.create(
            user=self.user,
            card=self.card,
            amount="500.00",
        )

        self.assertEqual(transaction.status, "PENDING")
