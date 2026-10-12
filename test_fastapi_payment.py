
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

import pytest
from django.contrib.auth import get_user_model
from fastapi.testclient import TestClient
from rest_framework_simplejwt.tokens import AccessToken

from cards.models import Card
from payment_api import app

User = get_user_model()
client = TestClient(app)


@pytest.fixture
def setup_user_card(transactional_db):
    user = User.objects.create_user(
        username="fastapitest",
        password="TestPass123!",
    )

    card = Card.objects.create(
        user=user,
        card_type="CREDIT",
        masked_card="************3456",
        last_four_digits="3456",
    )

    token = str(AccessToken.for_user(user))

    return user, card, token


def test_payment_api_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == (
        "CreditPay Payment API is running"
    )


def test_payment_requires_token(setup_user_card):
    _, card, _ = setup_user_card

    response = client.post(
        "/payments/",
        json={"card_id": card.id, "amount": 500},
    )

    assert response.status_code == 401


def test_payment_rejects_invalid_token(setup_user_card):
    _, card, _ = setup_user_card

    response = client.post(
        "/payments/",
        headers={"Authorization": "Bearer invalid-token"},
        json={"card_id": card.id, "amount": 500},
    )

    assert response.status_code == 401


def test_payment_succeeds_with_valid_token(setup_user_card):
    _, card, token = setup_user_card

    response = client.post(
        "/payments/",
        headers={"Authorization": f"Bearer {token}"},
        json={"card_id": card.id, "amount": 500},
    )

    print("DEBUG RESPONSE:", response.status_code, response.json())

    assert response.status_code == 200
    assert response.json()["status"] == "SUCCESS"


def test_payment_rejects_another_users_card(setup_user_card):
    _, _, token = setup_user_card

    other_user = User.objects.create_user(
        username="anotheruser",
        password="TestPass123!",
    )

    other_card = Card.objects.create(
        user=other_user,
        card_type="CREDIT",
        masked_card="************1111",
        last_four_digits="1111",
    )

    response = client.post(
        "/payments/",
        headers={"Authorization": f"Bearer {token}"},
        json={"card_id": other_card.id, "amount": 500},
    )

    assert response.status_code == 404


def test_payment_rejects_invalid_amount(setup_user_card):
    _, card, token = setup_user_card

    response = client.post(
        "/payments/",
        headers={"Authorization": f"Bearer {token}"},
        json={"card_id": card.id, "amount": 0},
    )

    assert response.status_code == 422


def test_payment_rejects_negative_amount(setup_user_card):
    _, card, token = setup_user_card

    response = client.post(
        "/payments/",
        headers={"Authorization": f"Bearer {token}"},
        json={"card_id": card.id, "amount": -100},
    )

    assert response.status_code == 422
