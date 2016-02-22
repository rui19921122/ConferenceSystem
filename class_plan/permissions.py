from rest_framework.permissions import BasePermission, SAFE_METHODS
from base.models import Department
from class_plan.models import WhichDepartmentCanEditClassPlan
from django.http import request


class IsAllowedOrReadOnly(BasePermission):
    """
    确保只有指定的人才可以执行不安全方法
    """
    message = '没有权限改正班计划'

    def has_permission(self, request, view):
        '''

        :rtype request: request
        :param view:
        :param obj:
        :return:
        '''
        if request.method in SAFE_METHODS:
            return True
        else:
            allowed_department = WhichDepartmentCanEditClassPlan.objects.all()
            user = request.user
            if allowed_department.filter(department=user.user.department).exists() or \
                    user.is_superuser:
                return True
            else:
                return False
