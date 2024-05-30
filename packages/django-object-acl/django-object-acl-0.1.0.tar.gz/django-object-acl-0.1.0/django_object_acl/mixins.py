from typing import List

from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import PermissionDenied
from django.db import models

from .managers import OwnedObjectsManager, PermittedObjectsManager
from .models import Permission


class PermittedModelMixin(models.Model):
    """
    Use this to add permissions for model
    Your model will have:
        * .permissions set with all permissions for a given instance
        * option to get permitted objects for a given auth object, mapping provided in settings
        * new attributes on each instance to indicate if the request user can view / edit / delete

    """

    objects = models.Manager()
    permitted_objects = PermittedObjectsManager()
    permissions = GenericRelation(
        Permission,
        content_type_field="content_type",
        object_id_field="object_pk",
        related_query_name="permissions",
    )

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: str = None,
        update_fields: List[str] = None,
    ) -> None:
        if not getattr(self, "can_edit", True):
            raise PermissionDenied
        super().save(force_insert, force_update, using, update_fields)

    def delete(self, using: str = None, keep_parents: bool = False) -> None:
        if not getattr(self, "can_delete", True):
            raise PermissionDenied
        super().delete(using, keep_parents)

    def _persist_permissions(
        self, grantee_type: str, grantee_value: str, perm_operations: List[str]
    ) -> None:
        permissions = []
        for perm_operation in perm_operations:
            permissions.append(
                Permission(
                    grantee_type=grantee_type,
                    grantee_value=grantee_value,
                    operation=perm_operation,
                    content_object=self,
                )
            )
        Permission.objects.bulk_create(permissions)

    def assign_view_permission(self, grantee_type: str, grantee_value: str) -> None:
        perm_operations = [Permission.OPERATION_VIEW]
        self._persist_permissions(grantee_type, grantee_value, perm_operations)

    def assign_edit_permission(self, grantee_type: str, grantee_value: str) -> None:
        perm_operations = [Permission.OPERATION_VIEW, Permission.OPERATION_EDIT]
        self._persist_permissions(grantee_type, grantee_value, perm_operations)

    def assign_all_permissions(self, grantee_type: str, grantee_value: str) -> None:
        self._persist_permissions(grantee_type, grantee_value, Permission.OPERATIONS)

    class Meta:
        abstract = True


class OwnedModelMixin(PermittedModelMixin):
    """
    Use to override create method requiring to provide an owner on object creation
    """

    permitted_objects = OwnedObjectsManager()

    class Meta:
        abstract = True
