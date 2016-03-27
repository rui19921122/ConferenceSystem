from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class OnlyOwnerDepartmentCanRead(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return request.user.user.department == obj.department
