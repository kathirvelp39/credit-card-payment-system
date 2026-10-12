from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from transactions.models import AdminLog

User = get_user_model()

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        AdminLog.objects.create(
            performed_by=request.user,
            action="UPDATE" if change else "CREATE",
            details=f"User {obj.username} saved",
        )

    def delete_model(self, request, obj):
        AdminLog.objects.create(
            performed_by=request.user,
            action="DELETE",
            details=f"User {obj.username} deleted",
        )
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        count = queryset.count()

        if count:
            AdminLog.objects.create(
                performed_by=request.user,
                action="DELETE",
                details=f"{count} users deleted",
            )

        queryset.delete()