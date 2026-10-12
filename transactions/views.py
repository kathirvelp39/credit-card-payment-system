from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Transaction
from .serializers import TransactionSerializer


class TransactionListView(
    generics.ListAPIView
):

    serializer_class = TransactionSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        queryset = (
            Transaction.objects
            .filter(user=self.request.user)
            .select_related("card")
            .order_by("-created_at")
        )

        # Status filter
        status_value = (
            self.request
            .query_params
            .get("status")
        )

        if status_value:
            queryset = queryset.filter(
                status=status_value.upper()
            )

        # Minimum amount
        min_amount = (
            self.request
            .query_params
            .get("min_amount")
        )

        if min_amount:
            queryset = queryset.filter(
                amount__gte=min_amount
            )

        # Maximum amount
        max_amount = (
            self.request
            .query_params
            .get("max_amount")
        )

        if max_amount:
            queryset = queryset.filter(
                amount__lte=max_amount
            )

        # From date filter
        from_date = (
            self.request
            .query_params
            .get("from_date")
        )

        if from_date:
            queryset = queryset.filter(
                created_at__date__gte=from_date
            )

        # To date filter
        to_date = (
            self.request
            .query_params
            .get("to_date")
        )

        if to_date:
            queryset = queryset.filter(
                created_at__date__lte=to_date
            )

        return queryset