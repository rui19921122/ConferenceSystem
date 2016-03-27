from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serialzation import WorkerSerial, PositionSerial
from .models import Worker, Position


# Create your views here.
class WorkerView(ListCreateAPIView):
    '''
    获取一个部门的所有人员，包括替班组和学员,只有部门的管理员或者超级管理员才可以查询或更改该部门信息
    支持方法:list,post
    参数:name str,position index,is_study bool,alter bool
    '''
    serializer_class = WorkerSerial

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Worker.objects.all()
        else:
            department = user.user.department
            return Worker.objects.filter(position__department=department)


class WorkerDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerial
    lookup_field = ('pk')
    # todo 增加权限管理


class PositionListView(ListCreateAPIView):
    '''
    获取一个部门的所有岗位和岗位数目,只有部门的管理员或者超级管理员才可以查询或更改该部门信息
    支持方法:list,post
    参数:id int,name str,number int
    '''
    serializer_class = PositionSerial

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Position.objects.all()
        else:
            department = user.user.department
            return Position.objects.filter(department=department)

    def perform_create(self, serializer):
        user = self.request.user
        department = user.user.department
        serializer.save(department=department)


class PositionDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = PositionSerial
    queryset = Position.objects.all()
    # todo 增加权限管理
