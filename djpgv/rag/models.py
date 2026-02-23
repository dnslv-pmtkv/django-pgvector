from django.db import models
from pgvector.django import HnswIndex, VectorField

from djpgv.core.models import BaseModel


class Collection(BaseModel):
    name = models.CharField(max_length=32)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Document(BaseModel):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="documents")
    embedding = VectorField(dimensions=1536)
    metadata = models.JSONField(default=dict)

    class Meta:
        indexes = [
            HnswIndex(
                name="clip_l14_vectors_index",
                fields=["embedding"],
                m=16,
                ef_construction=64,
                opclasses=["vector_cosine_ops"],
            )
        ]
