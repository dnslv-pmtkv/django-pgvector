from django.contrib import admin

from djpgv.rag.models import Collection, Document


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug"]
    search_fields = ["id", "name", "slug"]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["id", "collection"]
    search_fields = ["id", "collection"]
