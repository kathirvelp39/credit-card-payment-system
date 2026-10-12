
from django.contrib import admin

from transactions.models import AdminLog

from .models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "card_type",
        "masked_card",
        "last_four_digits",
        "created_at",
    ]

    list_filter = [
        "card_type",
        "created_at",
    ]

    search_fields = [
        "user__username",
        "last_four_digits",
    ]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        AdminLog.objects.create(
            performed_by=request.user,
            action="UPDATE" if change else "CREATE",
            details=f"Card {obj.pk} saved",
        )

    def delete_model(self, request, obj):
        AdminLog.objects.create(
            performed_by=request.user,
            action="DELETE",
            details=f"Card {obj.pk} deleted",
        )

        super().delete_model(request, obj)