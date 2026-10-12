from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(
    serializers.ModelSerializer
):

    card_number = serializers.CharField(
        source="card.last_four_digits",
        read_only=True,
    )

    card_type = serializers.CharField(
        source="card.card_type",
        read_only=True,
    )

    class Meta:
        model = Transaction

        fields = [
            "id",
            "card_number",
            "card_type",
            "amount",
            "status",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "card_number",
            "card_type",
            "amount",
            "status",
            "created_at",
        ]