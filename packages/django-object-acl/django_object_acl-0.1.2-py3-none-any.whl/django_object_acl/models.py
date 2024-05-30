import uuid
from typing import Optional

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class BaseModel(models.Model):
    id: uuid.UUID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, editable=False
    )
    updated_at: models.DateTimeField = models.DateTimeField(
        auto_now=True, editable=False
    )

    class Meta:
        abstract = True
        ordering = ("-created_at",)


class PermissionTemplate(BaseModel):
    owner_grantee_type: str = models.CharField(max_length=255)
    owner_grantee_value: str = models.CharField(max_length=255)

    target_grantee_type: str = models.CharField(max_length=255)
    target_grantee_value: str = models.CharField(max_length=255)

    target_operation: str = models.CharField(max_length=10, blank=True)
    content_type: Optional[ContentType] = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        help_text="if empty, will apply for every content type",
        null=True,
    )

    class Meta:
        indexes = [
            models.Index(fields=["content_type"]),
        ]


class Permission(BaseModel):
    OPERATION_VIEW = "view"
    OPERATION_EDIT = "edit"
    OPERATION_DELETE = "delete"
    OPERATIONS = [
        OPERATION_VIEW,
        OPERATION_EDIT,
        OPERATION_DELETE,
    ]

    grantee_type: str = models.CharField(max_length=255)
    grantee_value: str = models.CharField(max_length=255)

    content_type: ContentType = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="permissions"
    )
    object_pk: uuid.UUID = models.UUIDField(editable=False)
    content_object: models.Model = GenericForeignKey(fk_field="object_pk")

    operation: str = models.CharField(max_length=10, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_pk"]),
        ]
