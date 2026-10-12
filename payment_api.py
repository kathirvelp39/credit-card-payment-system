
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

import jwt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field
from starlette.middleware.cors import CORSMiddleware

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.settings import api_settings

from cards.models import Card
from transactions.models import Transaction

app = FastAPI(
    title="CreditPay Payment API",
    description="Secure payment processing service",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer(auto_error=False)
User = get_user_model()


class PaymentRequest(BaseModel):
    card_id: int = Field(gt=0)
    amount: float = Field(gt=0)


class PaymentResponse(BaseModel):
    transaction_id: int
    user_id: int
    card_id: int
    amount: float
    status: str


def get_authenticated_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
):
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication token required.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(
            credentials.credentials,
            api_settings.SIGNING_KEY,
            algorithms=[api_settings.ALGORITHM],
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get(api_settings.USER_ID_CLAIM)

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token payload.",
        )

    try:
        user = User.objects.get(
            pk=user_id,
            is_active=True,
        )
    except (User.DoesNotExist, ValueError, TypeError):
        raise HTTPException(
            status_code=401,
            detail="User not found or inactive.",
        )

    return user


@app.get("/")
def home():
    return {"message": "CreditPay Payment API is running"}


@app.post("/payments/", response_model=PaymentResponse)
def make_payment(
    payment: PaymentRequest,
    current_user=Depends(get_authenticated_user),
):
    try:
        card = Card.objects.get(
            id=payment.card_id,
            user=current_user,
        )
    except Card.DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Card not found for this user.",
        )

    transaction = Transaction.objects.create(
        user=current_user,
        card=card,
        amount=payment.amount,
        status="PENDING",
    )

    if payment.amount <= 10000:
        transaction.status = "SUCCESS"
    else:
        transaction.status = "FAILED"

    transaction.save()

    return {
        "transaction_id": transaction.id,
        "user_id": current_user.id,
        "card_id": card.id,
        "amount": float(transaction.amount),
        "status": transaction.status,
    }
