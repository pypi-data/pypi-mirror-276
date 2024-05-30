from functools import reduce
from operator import ior
from typing import Any, Generator, List

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Case, Count, Manager, Model, Q, QuerySet, When

from .models import Permission, PermissionTemplate


class PermittedObjectsManager(Manager):
    def for_given(self, auth: Any) -> QuerySet:
        """
        Use to fetch objects by permissions and annotate permissions count by type to later determine if user can perform actions
        """
        queryset = super().get_queryset()

        lst: List[Q] = []
        for grantee_type, auth_func in getattr(
            settings, "DJANGO_OBJECT_ACL_PERMISSION_GRANTEE_TYPES", {}
        ).items():
            lst.append(
                Q(
                    permissions__grantee_type=grantee_type,
                    permissions__grantee_value=auth_func(auth),
                )
            )

        grantee_filter = reduce(ior, lst)

        return (
            queryset.filter(grantee_filter)
            .annotate(
                view_perm_count=Count(
                    "permissions",
                    filter=Q(permissions__operation=Permission.OPERATION_VIEW),
                )
            )
            .annotate(
                edit_perm_count=Count(
                    "permissions",
                    filter=Q(permissions__operation=Permission.OPERATION_EDIT),
                )
            )
            .annotate(
                delete_perm_count=Count(
                    "permissions",
                    filter=Q(permissions__operation=Permission.OPERATION_DELETE),
                )
            )
            .annotate(
                can_view=Case(
                    When(view_perm_count__gt=0, then=True),
                    default=False,
                    output_field=models.BooleanField(),
                )
            )
            .annotate(
                can_edit=Case(
                    When(edit_perm_count__gt=0, then=True),
                    default=False,
                    output_field=models.BooleanField(),
                )
            )
            .annotate(
                can_delete=Case(
                    When(delete_perm_count__gt=0, then=True),
                    default=False,
                    output_field=models.BooleanField(),
                )
            )
        )


class OwnedObjectsManager(PermittedObjectsManager):
    def create(
        self, auth: Any = None, owner_grantee_type: str = None, **kwargs: Any
    ) -> Model:
        owner_grantee_value: str = self._get_owner_grantee_value(
            auth, owner_grantee_type
        )
        obj = super().create(**kwargs)
        self._add_permissions(obj, owner_grantee_type, owner_grantee_value)
        return obj

    def _get_owner_grantee_value(self, auth: Any, owner_grantee_type: str) -> str:
        grantee_types = getattr(
            settings, "DJANGO_OBJECT_ACL_PERMISSION_GRANTEE_TYPES", {}
        )

        if owner_grantee_type not in grantee_types:
            raise ValueError(f"Invalid grantee type provided: {owner_grantee_type}")

        auth_func = grantee_types[owner_grantee_type]
        owner_grantee_value = auth_func(auth)

        if owner_grantee_value is None:
            raise ValueError(f"Invalid grantee value provided: {owner_grantee_value}")
        return owner_grantee_value

    def _add_permissions(
        self, obj: Model, owner_grantee_type: str, owner_grantee_value: str
    ) -> None:
        permissions = []

        for perm_operation in Permission.OPERATIONS:
            permissions.append(
                Permission(
                    grantee_type=owner_grantee_type,
                    grantee_value=owner_grantee_value,
                    operation=perm_operation,
                    content_object=obj,
                )
            )
        template_based_permissions = list(
            self._add_template_based_permissions(
                permissions, owner_grantee_type, owner_grantee_value
            )
        )
        permissions.extend(template_based_permissions)

        obj.permissions.bulk_create(permissions)

    def _add_template_based_permissions(
        self,
        created_permissions: List[Permission],
        owner_grantee_type: str,
        owner_grantee_value: str,
    ) -> Generator[Permission, None, None]:
        """
        Create permissions from permission templates
        Need to allow in settings to use
        """
        if not getattr(settings, "DJANGO_OBJECT_ACL_ALLOW_TEMPLATES", False):
            return

        permission_templates = PermissionTemplate.objects.filter(
            Q(content_type=None)
            | Q(content_type=ContentType.objects.get_for_model(self.model)),
            owner_grantee_type=owner_grantee_type,
            owner_grantee_value=owner_grantee_value,
        )

        for pt in permission_templates:
            for created_permission in created_permissions:
                yield Permission(
                    content_object=created_permission.content_object,
                    operation=pt.target_operation,
                    grantee_type=pt.target_grantee_type,
                    grantee_value=pt.target_grantee_value,
                )
