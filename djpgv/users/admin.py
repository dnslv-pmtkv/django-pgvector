from django.contrib import admin

from djpgv.users.models import User


@admin.register(User)
class BaseUserAdmin(admin.ModelAdmin):
    list_display = ["email", "is_superuser", "created_at", "updated_at"]
    search_fields = ["email"]
    list_filter = ["is_superuser"]
    readonly_fields = ["last_login", "created_at", "updated_at"]

    fieldsets = (
        (None, {"fields": ["email", "last_login", "is_superuser"]}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
