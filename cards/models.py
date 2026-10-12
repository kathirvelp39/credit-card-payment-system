from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models


class Card(models.Model):
    CARD_TYPES = (
        ("CREDIT", "Credit"),
        ("DEBIT", "Debit"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cards",
    )

    card_type = models.CharField(
        max_length=10,
        choices=CARD_TYPES,
    )

    masked_card = models.CharField(max_length=19)

    last_four_digits = models.CharField(max_length=4)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.card_type} - {self.masked_card}"