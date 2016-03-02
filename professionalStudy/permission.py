from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class OnlyOwnerDepartmentCanEdit(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.user.department == obj.department
