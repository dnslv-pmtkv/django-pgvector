from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey("users.User", blank=True, null=True, related_name="+", on_delete=models.SET_NULL)
    updated_by = models.ForeignKey("users.User", blank=True, null=True, related_name="+", on_delete=models.SET_NULL)

    class Meta:
        abstract = True
