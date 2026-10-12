
from django.conf import settings
from django.db import models

from cards.models import Card


class Transaction(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions",
    )

    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name="transactions",
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="PENDING",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"₹{self.amount} - "
            f"{self.status}"
        )


class AdminLog(models.Model):
    ACTION_CHOICES = (
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
    )

    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="admin_logs",
    )

    action = models.CharField(
        max_length=10,
        choices=ACTION_CHOICES,
    )

    details = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.action} - {self.details}"
