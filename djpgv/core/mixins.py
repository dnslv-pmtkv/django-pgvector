from typing import TYPE_CHECKING, Sequence, Type

from rest_framework.permissions import BasePermission, IsAuthenticated

if TYPE_CHECKING:
    # This is going to be resolved in the stub library
    # https://github.com/typeddjango/djangorestframework-stubs/
    from rest_framework.permissions import _PermissionClass

    PermissionClassesType = Sequence[_PermissionClass]
else:
    PermissionClassesType = Sequence[Type[BasePermission]]


class PrivateApiMixin:
    permission_classes: PermissionClassesType = (IsAuthenticated,)


class PublicApiMixin:
    authentication_classes = []
    permission_classes = []
