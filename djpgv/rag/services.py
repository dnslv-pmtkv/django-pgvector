from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.utils.text import slugify

from djpgv.core.services import ModelUpdateReturnValue, model_update
from djpgv.rag.models import Collection


def collection_create(*, name: str) -> Collection:
    random_suffix = get_random_string(length=8)
    slug = slugify(name + random_suffix)

    collection = Collection(name=name, slug=slug)
    collection.full_clean()
    collection.save()

    return collection


class CollectionService:
    def _slugify_name(self, *, name: str):
        random_suffix = get_random_string(length=8)
        slug = slugify(f"{name}-{random_suffix}")

        return slug

    def create(self, *, name: str) -> Collection:
        slug = self._slugify_name(name=name)

        collection = Collection(name=name, slug=slug)
        collection.full_clean()
        collection.save()

        return collection

    def retrieve(self, *, slug: str, get: bool = False) -> Collection | QuerySet[Collection]:
        collection_filter = Collection.objects.filter(slug=slug)

        if get:
            return get_object_or_404(collection_filter)

        return collection_filter

    def update(self, *, collection: Collection, name: str) -> ModelUpdateReturnValue:
        update_data = {"name": name}

        if name != collection.name:
            slug = self._slugify_name(name=name)
            update_data["slug"] = slug

        return model_update(instance=collection, data=update_data)

    def delete(self, *, slug: str) -> None:
        self.retrieve(slug=slug).delete()
