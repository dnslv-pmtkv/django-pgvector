from dataclasses import dataclass
from typing import Any, Dict

from django.db import models

from djpgv.core.types import DjangoModelType
from djpgv.core.utils import get_now


@dataclass
class ModelUpdateReturnValue:
    instance: DjangoModelType
    has_updated: bool


def model_update(*, instance: DjangoModelType, data: Dict[str, Any], auto_updated_at=True) -> ModelUpdateReturnValue:
    updated_at_field = "updated_at"
    has_updated = False
    m2m_data = {}
    data_fields = list(data.keys())
    update_fields = []
    model_fields = {field.name: field for field in instance._meta.get_fields()}

    for field in data_fields:
        model_field = model_fields.get(field)

        assert model_field is not None, f'{instance.__class__.__name__} has no field "{field}".'

        if isinstance(model_field, models.ManyToManyField):
            m2m_data[field] = data[field]
            continue

        if getattr(instance, field) != data[field]:
            has_updated = True
            update_fields.append(field)
            setattr(instance, field, data[field])

    if has_updated:
        if auto_updated_at and updated_at_field in model_fields and updated_at_field not in update_fields:
            update_fields.append(updated_at_field)
            instance.updated_at = get_now()

        instance.full_clean()
        instance.save(update_fields=update_fields)

    for field_name, value in m2m_data.items():
        related_manager = getattr(instance, field_name)
        related_manager.set(value)

        has_updated = True

    return ModelUpdateReturnValue(instance=instance, has_updated=has_updated)
