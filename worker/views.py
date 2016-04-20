from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Worker, Position, FigureSetting, Figure
from .serialzation import WorkerSerial, PositionSerial


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


class FigureCollect(APIView):
    '''
    上传或删除指纹，支持方法post,delete
    '''

    def post(self, request: Request, *args, **kwargs):
        department = request.user.user.department
        try:
            setting = FigureSetting.objects.get(department=department)
        except:
            return Response(data={'error': '抱歉，未对此部门分配权限，请联系管理员添加'}, status=status.HTTP_403_FORBIDDEN)
        if not setting.can_add:
            return Response(data={'error': '抱歉，可添加权限被设置为否'}, status=status.HTTP_403_FORBIDDEN)
        worker_id = request.data['id']
        name = request.data['name']
        try:
            value = request.data['value'].encode('utf-8')
        except:
            return Response(data={'error': 'value不是有效的字符'}, status=status.HTTP_400_BAD_REQUEST)
        worker = Worker.objects.get(pk=worker_id)
        if department == worker.position.department:
            if worker.figures.filter(name=name).exists():
                print(worker.figures.all())
                return Response(data={'error': '抱歉，系统内已有此员工指纹，请勿重复录入'}, status=status.HTTP_403_FORBIDDEN)
            new = Figure(modal=value, name=name)
            new.save()
            worker.figures.add(new)
            worker_data = Worker.objects.get(pk=worker_id)
            ser = WorkerSerial(worker_data)
            return Response(ser.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'error': '抱歉，您没有合适的权限访问此职工信息'}, status=status.HTTP_403_FORBIDDEN)
        pass

    def delete(self, request: Request, *args, **kwargs):
        department = request.user.user.department
        try:
            setting = FigureSetting.objects.get(department=department)
        except:
            return Response(data={'error': '抱歉，未对此部门分配权限，请联系管理员添加'}, status=status.HTTP_403_FORBIDDEN)
        if not setting.can_delete:
            return Response(data={'error': '抱歉，可删除权限被设置为否'}, status=status.HTTP_403_FORBIDDEN)
        worker_id = request.data['id']
        name = request.data['name']
        worker = Worker.objects.get(pk=worker_id)
        if department == worker.position.department:
            try:
                figure = worker.figures.get(name=name)
                figure.delete()
            except:
                pass
            worker_data = Worker.objects.get(pk=worker_id)
            ser = WorkerSerial(worker_data)
            return Response(ser.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(data={'error': '抱歉，您没有合适的权限访问此职工信息'}, status=status.HTTP_403_FORBIDDEN)
