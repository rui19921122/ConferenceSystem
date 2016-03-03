from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serialzation import WorkSerializetion
from .models import Worker


# Create your views here.
class WorkerView(ListCreateAPIView):
    '''
    获取一个部门的所有人员，包括替班组和学员,只有部门的管理员或者超级管理员才可以查询或更改该部门信息
    支持方法:list,post
    参数:name str,position index,is_study bool,alter bool
    '''
    serializer_class = WorkSerializetion

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Worker.objects.all()
        else:
            department = user.user.department
            return Worker.objects.filter(position__department=department)


class WorkerDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = WorkSerializetion
    # todo 增加权限管理
