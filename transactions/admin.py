import csv

from django.contrib import admin
from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncDate
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import path

from .models import AdminLog, Transaction


@admin.action(description="Export selected transactions to CSV")
def export_transactions_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        'attachment; filename="transactions.csv"'
    )

    writer = csv.writer(response)
    writer.writerow([
        "Transaction ID",
        "User",
        "Card",
        "Amount",
        "Status",
        "Created At",
    ])

    for transaction in queryset:
        writer.writerow([
            transaction.id,
            transaction.user.username,
            transaction.card.last_four_digits,
            transaction.amount,
            transaction.status,
            transaction.created_at,
        ])

    return response


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    change_list_template = (
        "admin/transactions/transaction/change_list.html"
    )

    list_display = [
        "id",
        "user",
        "card",
        "amount",
        "status",
        "created_at",
    ]

    list_filter = ["status", "created_at"]
    search_fields = ["user__username", "card__last_four_digits"]
    actions = [export_transactions_csv]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        AdminLog.objects.create(
            performed_by=request.user,
            action="UPDATE" if change else "CREATE",
            details=f"Transaction {obj.pk} saved",
        )

    def delete_model(self, request, obj):
        AdminLog.objects.create(
            performed_by=request.user,
            action="DELETE",
            details=f"Transaction {obj.pk} deleted",
        )
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        count = queryset.count()

        if count:
            AdminLog.objects.create(
                performed_by=request.user,
                action="DELETE",
                details=f"{count} transactions deleted",
            )

        queryset.delete()

    def get_urls(self):
        custom_urls = [
            path(
                "daily-summary/",
                self.admin_site.admin_view(self.daily_summary_view),
                name="transactions_transaction_daily_summary",
            ),
        ]
        return custom_urls + super().get_urls()

    def daily_summary_view(self, request):
        daily_summaries = (
            Transaction.objects
            .annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(
                total_transactions=Count("id"),
                successful_payments=Count(
                    "id",
                    filter=Q(status="SUCCESS"),
                ),
                failed_payments=Count(
                    "id",
                    filter=Q(status="FAILED"),
                ),
                successful_amount=Sum(
                    "amount",
                    filter=Q(status="SUCCESS"),
                ),
            )
            .order_by("-day")
        )

        context = {
            **self.admin_site.each_context(request),
            "title": "Daily Payment Summary",
            "daily_summaries": daily_summaries,
            "opts": self.model._meta,
        }

        return TemplateResponse(
            request,
            "admin/transactions/daily_summary.html",
            context,
        )


@admin.register(AdminLog)
class AdminLogAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "performed_by",
        "action",
        "details",
        "created_at",
    ]

    list_filter = ["action", "created_at"]
    search_fields = ["performed_by__username", "details"]

    readonly_fields = [
        "performed_by",
        "action",
        "details",
        "created_at",
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False