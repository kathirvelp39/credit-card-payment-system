from rest_framework import serializers

from .models import Card


class CardSerializer(serializers.ModelSerializer):
    card_number = serializers.CharField(
        write_only=True,
        min_length=13,
        max_length=19,
    )

    class Meta:
        model = Card
        fields = [
            "id",
            "card_type",
            "card_number",
            "masked_card",
            "last_four_digits",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "masked_card",
            "last_four_digits",
            "created_at",
        ]

    def validate_card_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError(
                "Card number must contain only digits."
            )

        if len(value) not in range(13, 20):
            raise serializers.ValidationError(
                "Card number must be between 13 and 19 digits."
            )

        return value

    def create(self, validated_data):
        card_number = validated_data.pop("card_number")

        masked_card = "*" * (len(card_number) - 4) + card_number[-4:]

        return Card.objects.create(
            user=self.context["request"].user,
            card_type=validated_data["card_type"],
            masked_card=masked_card,
            last_four_digits=card_number[-4:],
        )