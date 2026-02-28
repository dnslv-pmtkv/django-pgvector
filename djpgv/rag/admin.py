from typing import Any

from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.http import HttpRequest

from djpgv.rag.models import Chunk, Collection, Document
from djpgv.rag.services import CollectionService


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug"]
    search_fields = ["id", "name", "slug"]
    readonly_fields = ["slug", "created_at", "updated_at", "created_by", "updated_by"]

    def save_model(self, request: HttpRequest, obj, form: Any, change: Any) -> None:
        service = CollectionService()

        if change:
            collection = service.retrieve(slug=obj.slug, get=True)
            return service.update(collection=collection, **form.cleaned_data)

        try:
            service.create(**form.cleaned_data)
        except ValidationError as exception:
            self.message_user(request, str(exception), messages.ERROR)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["id", "collection"]
    search_fields = ["id", "collection"]


@admin.register(Chunk)
class ChunkAdmin(admin.ModelAdmin):
    list_display = ["id", "document", "content"]
    search_fields = ["id", "document"]
