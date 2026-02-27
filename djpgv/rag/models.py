from django.db import models
from pgvector.django import HnswIndex, VectorField

from djpgv.core.models import BaseModel


class Collection(BaseModel):
    name = models.CharField(max_length=32)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Document(BaseModel):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="documents")
    title = models.CharField(max_length=255)
    content = models.TextField()
    version = models.CharField(max_length=32)


class Chunk(BaseModel):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="chunks")
    content = models.TextField()
    embedding = VectorField(dimensions=1536)
    metadata = models.JSONField(default=dict)

    class Meta:
        indexes = [
            HnswIndex(
                name="chunk_embedding_hnsw",
                fields=["embedding"],
                opclasses=["vector_cosine_ops"],
            ),
        ]
