import ctypes
import time
import datetime

from django.core import exceptions
from django.db.models import Q
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accidentCase.models import Accident
from accidentCase.serization import AccidentSerializer
from class_plan.models import ClassPlanDayTable
from class_plan.serialzation import ClassPlanDayTable as ClassPlanDayTableSer
from professionalStudy.models import ProfessionalStudy
from professionalStudy.serialzation import ProfessionalStudySerializer
from worker.models import AttentionTable, Worker, AttentionDetail, Position
from .models import CallOverDetail
from .models import CallOverNumber
from .permission import OnlyOwnerDepartmentCanRead
from .serialzation import PhotoSer, AudioSer, WorkerSer, CallOverSer, AttentionSer, AttentionsDetailSer

windll = ctypes.windll.JZTDevDll


def exam_equal_figure(source, string):
    f = windll.FPIMatch(source.encode('utf-8'), string.encode('utf-8'), 3)
    return True if f >= 0 else False


def get_current_class():
    # 获取当前班组，若不在规定时间可直接报错
    current_date = datetime.date.today()
    hour = datetime.datetime.now().hour
    day_number = 1 if hour < 12 else 2
    return CallOverNumber.objects.get(date=current_date, day_number=day_number)


# Create your views here.
class GetDefaultClassNumber(APIView):
    def get(self, request):
        '''
        :param request:Request
        :return:
        '''
        user = request.user
        if user.is_authenticated():
            try:
                number = get_current_class().class_number
                return Response({'number': number}
                                , status=status.HTTP_200_OK)
            except:
                return Response({'number': False}
                                , status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


mapNumberToQuery = {
    '1': 'checked_by_first',
    '2': 'checked_by_second',
    '3': 'checked_by_third',
    '4': 'checked_by_forth',
}


class BeginCallOver(APIView):
    '''
        开始点名，无必须field
    '''

    def post(self, request):
        '''
        :param request:Request
        :return:
        '''
        user = request.user
        department = user.user.department
        if not user.is_authenticated():
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            default_class_number = get_current_class()
        except:
            return Response('不是规定的时间段', status=status.HTTP_400_BAD_REQUEST)
        default = get_current_class()
        today = datetime.datetime.today()
        try:
            attention_table = AttentionTable.objects.get(date=default.date, department=department,
                                                         day_number=default.day_number)
            locked = attention_table.lock
        except:
            return Response("未找到相关的预点名信息", status=status.HTTP_404_NOT_FOUND)
        if not locked:
            return Response("出勤表未锁定，无法进行点名", status=status.HTTP_400_BAD_REQUEST)
        number = str(request.data.get('number', default.class_number))
        query = mapNumberToQuery[number]
        # 处理添加相关人员
        exist = CallOverDetail.objects.filter(department=department,
                                              date=today,
                                              # 使用day_number 会多一次数据库查询，可优化
                                              day_number=default_class_number.day_number)
        if not exist:
            new = CallOverDetail.objects.create(department=department,
                                                host_person=user,
                                                class_number=number,
                                                attend_table=attention_table,
                                                day_number=default_class_number.day_number)
            pk = new.pk
            exist = new
        else:
            exist = exist[0]
            if exist.end_time:
                return Response("本次考勤已结束，无法开始", status=status.HTTP_400_BAD_REQUEST)
            pk = exist.pk
            try:
                class_plan = ClassPlanDayTable.objects.get(time=today)
                if not class_plan.lock:  # 如果班计划表未锁定，则对其进行锁定
                    class_plan.lock = True
                    class_plan.save()
            except:
                class_plan = None
            args_not_need_edit = {'department': department,
                                  query: exist,
                                  }
            had_study = ProfessionalStudy.objects.filter(**args_not_need_edit)
            had_accident = Accident.objects.filter(**args_not_need_edit)
            class_plan_ser = ClassPlanDayTableSer(class_plan)
            study_ser = ProfessionalStudySerializer(had_study, many=True)
            accident_ser = AccidentSerializer(had_accident, many=True)
            return Response({'data': {'class_plan': class_plan_ser.data,
                                      'study': study_ser.data,
                                      'accident': accident_ser.data,},
                             'pk': pk})

        # 处理回送数据
        try:
            class_plan = ClassPlanDayTable.objects.get(time=today)
        except:
            class_plan = None
        args_edit = {'department': department, query + '__isnull': True}
        un_study = ProfessionalStudy.objects.filter(**args_edit)
        if un_study:
            for i in un_study:
                i.study(number, exist)
        args_not_need_edit = {'department': department,
                              query: exist,
                              }
        had_study = ProfessionalStudy.objects.filter(**args_not_need_edit)
        un_accident = Accident.objects.filter(**args_edit)
        if un_accident:
            for i in un_accident:
                i.study(number, exist)
        had_accident = Accident.objects.filter(**args_not_need_edit)
        class_plan_ser = ClassPlanDayTableSer(class_plan)
        study_ser = ProfessionalStudySerializer(had_study, many=True)
        accident_ser = AccidentSerializer(had_accident, many=True)
        return Response({'data': {'class_plan': class_plan_ser.data,
                                  'study': study_ser.data,
                                  'accident': accident_ser.data,},
                         'pk': pk})


class EndCallOver(APIView):
    '''
        结束点名，无必须field
    '''

    def post(self, request):
        '''
        :param request:Request
        :return:
        '''
        user = request.user
        department = user.user.department
        if not user.is_authenticated():
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            default_class_number = get_current_class()
        except:
            return Response('不是规定的时间段', status=status.HTTP_400_BAD_REQUEST)
        default = get_current_class()
        today = datetime.datetime.today()
        number = str(request.data.get('number', default.class_number))
        query = mapNumberToQuery[number]
        # 处理添加相关人员
        exist = CallOverDetail.objects.filter(department=department,
                                              date=today,
                                              # 使用day_number 会多一次数据库查询，可优化
                                              day_number=default_class_number.day_number)
        if not exist:
            return Response({'error': '未发现点名数据'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            exist = exist[0]
            if exist.end_time:
                return Response({'error': '本次考勤已经结束，请不要再次结束'}, status=status.HTTP_400_BAD_REQUEST)
            exist.end_time = datetime.datetime.now()
            exist.save()
            return Response(status=status.HTTP_202_ACCEPTED)


class QueryCallOverByDepartment(APIView):
    def get(self, request: Request, id):
        try:
            call_over = CallOverDetail.objects.get(pk=id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user = request.user
        department = user.user.department
        if department == call_over.department:
            pass
        elif request.user.is_superuser:
            pass
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            class_plan = ClassPlanDayTable.objects.get(time=call_over.date)
        except:
            class_plan = None
        study = ProfessionalStudy.objects.filter(
            Q(checked_by_first=call_over)
            | Q(checked_by_second=call_over)
            | Q(checked_by_third=call_over)
            | Q(checked_by_forth=call_over)
        )
        accident = Accident.objects.filter(
            Q(checked_by_first=call_over)
            | Q(checked_by_second=call_over)
            | Q(checked_by_third=call_over)
            | Q(checked_by_forth=call_over)
        )
        audios = call_over.audios_set.all()
        photos = call_over.photos_set.all()
        audio_ser = AudioSer(audios, many=True)
        photo_ser = PhotoSer(photos, many=True)
        class_plan_ser = ClassPlanDayTableSer(class_plan)
        study_ser = ProfessionalStudySerializer(study, many=True)
        accident_ser = AccidentSerializer(accident, many=True)
        used_ser = WorkerSer(call_over.attend_person_used.all(), many=True)
        unused_ser = WorkerSer(call_over.attend_person_unused.all(), many=True)
        return Response({'data': {'class_plan': class_plan_ser.data,
                                  'study': study_ser.data,
                                  'accident': accident_ser.data,},
                         'audio': audio_ser.data,
                         'person': {'used': used_ser.data,
                                    'unused': unused_ser.data},
                         'meta': {'begin': call_over.begin_time,
                                  'end': call_over.end_time,
                                  'host': call_over.host_person.user.name},
                         'photo': photo_ser.data})


class ListClassOverByDepartment(generics.ListAPIView, generics.GenericAPIView):
    queryset = CallOverDetail
    serializer_class = CallOverSer
    permission_classes = (OnlyOwnerDepartmentCanRead,)

    def list(self, request: Request, *args, **kwargs):
        begin_time = request.GET.get('start', default=datetime.date.today())
        end_time = request.GET.get('end', default=datetime.date.today())
        if request.user.is_superuser:
            obj = CallOverDetail.objects.filter(date__lte=end_time, date__gte=begin_time)
        else:
            obj = CallOverDetail.objects.filter(department=request.user.user.department,
                                                date__lte=end_time,
                                                date__gte=begin_time)
        return Response(data=CallOverSer(obj, many=True).data, status=status.HTTP_200_OK)


class GetCallOverPerson(generics.ListAPIView, generics.GenericAPIView):
    '''
    '''
    queryset = AttentionTable
    serializer_class = AttentionSer

    def list(self, request: Request, *args, **kwargs):
        default = get_current_class()
        date = request.GET.get('date', default=default.date)
        day_number = request.GET.get('day-number', default=default.day_number)
        department = request.user.user.department
        try:
            attention_table = AttentionTable.objects.get(date=date, day_number=day_number, department=department)
        except exceptions.ObjectDoesNotExist:
            department = request.user.user.department
            workers = Worker.objects.filter(position__department=request.user.user.department,
                                            class_number=CallOverNumber.objects.get(date=date,
                                                                                    day_number=day_number).class_number)
            attention_table = AttentionTable(department=department, date=date, day_number=day_number, lock=False)
            attention_table.save()
            for worker in workers:
                new = AttentionDetail(
                    worker=worker,
                    position=worker.position,
                    study=worker.is_study,
                )
                new.save()
                attention_table.person.add(new)
        can_add_workers = Worker.objects.all()
        had_attention = attention_table.person.all()
        for worker in had_attention:
            can_add_workers = can_add_workers.exclude(pk=worker.worker_id)
        can_add_workers.filter(position__department=request.user.user.department)
        return Response(data={'attend': self.get_serializer_class()(attention_table).data,
                              'id': attention_table.id,
                              'lock': attention_table.lock,
                              'replace': WorkerSer(can_add_workers, many=True).data},
                        status=status.HTTP_200_OK)


class UpdateCallOverPerson(APIView):
    """
        用于更改未被锁定的考勤表职工情况，其中，学员只能被删除，非学员的职位只能被替换，替换参数为replace,内容为职工ID
    """
    # todo 目前没有卡控已有的人员重复录制的问题
    permission_classes = (OnlyOwnerDepartmentCanRead,)

    def post(self, request: Request, id, *args, **kwargs):
        attention_detail = AttentionDetail.objects.get(pk=id)
        if attention_detail.attentiontable_set.first().lock:
            return Response(data={'error': '考勤表已锁定，无法更改'}, status=status.HTTP_400_BAD_REQUEST)
        replace_id = request.data.get('replace')
        print(replace_id)
        try:
            replace_worker = Worker.objects.get(pk=replace_id)
        except exceptions.ObjectDoesNotExist:
            return Response(data={'error': '无法找到对应的职工'}, status=status.HTTP_400_BAD_REQUEST)
        if replace_worker.position.department == attention_detail.position.department:
            attention_detail.worker = replace_worker
            attention_detail.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(data={'error': '无法找到对应的职工'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, id, *args, **kwargs):
        attention_detail = AttentionDetail.objects.get(pk=id)
        if attention_detail.attentiontable_set.first().lock:
            return Response(data={'error': '考勤表已锁定，无法更改'}, status=status.HTTP_400_BAD_REQUEST)
        if not attention_detail.study:
            return Response(data={'error': '非学员的项目不能删除'}, status=status.HTTP_400_BAD_REQUEST)
        attention_detail.delete()
        return Response(status=status.HTTP_202_ACCEPTED)


class AddCallOverPerson(APIView):
    """
        向考勤表中增加信息，只能增加学员
        position:position_id,
        worker:worker_id
    """
    permission_classes = (OnlyOwnerDepartmentCanRead,)

    def post(self, request: Request, id, *args, **kwargs):
        _position = request.data.get('position')
        _worker = request.data.get('worker')
        attention_table = AttentionTable.objects.get(pk=id)
        position = Position.objects.get(id=_position)
        worker = Worker.objects.get(id=_worker)
        department = request.user.user.department
        if (position.department == department) and (attention_table.department == department) and (
                    worker.position.department == department):
            pass
        else:
            return Response(data={'error': '错误的部门信息'}, status=status.HTTP_400_BAD_REQUEST)
        new = AttentionDetail(worker=worker, position=position, study=True)
        new.save()
        attention_table.person.add(new)
        print(attention_table.person.all())
        return Response(status=status.HTTP_201_CREATED)


class GetCallOverPersonDetail(APIView):
    def get(self, request: Request, *args, **kwargs):
        department = request.user.user.department
        try:
            attention_number = self.request.GET.get('number')
        except:
            return Response(data={"error": "number字符串缺失"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            obj = AttentionTable.objects.get(pk=attention_number)
        except:
            return Response(data={"error": "未找到相关预点名信息"}, status=status.HTTP_404_NOT_FOUND)
        if obj.department != department:
            return Response(data={"error": "无权访问"}, status=status.HTTP_403_FORBIDDEN)
        ser = AttentionsDetailSer(obj.person.all(), many=True)
        return Response(data=ser.data, status=status.HTTP_200_OK)


class PostFigureData(APIView):
    '''
        向服务器传输指纹信息,有两个字段构成,figure_data 为指纹模型，number为预点名ID,如点名成功则返回201，失败返回400+，错误在error字段里
    '''

    def post(self, request: Request, *args, **kwargs):
        department = request.user.user.department
        figure_data = request.POST.get('figure_data')
        number = request.POST.get('number')
        if not figure_data:
            return Response(data={'error': 'figure_data字段缺失'}, status=status.HTTP_400_BAD_REQUEST)
        if not number:
            return Response(data={'error': 'number字段缺失'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            obj = AttentionTable.objects.get(pk=number)
        except:
            return Response(data={"error": "未找到相关预点名信息"}, status=status.HTTP_404_NOT_FOUND)
        if obj.department != department:
            return Response(data={"error": "无权访问"}, status=status.HTTP_403_FORBIDDEN)
        if not obj.lock:
            return Response(data={"error": "尚未锁定出勤表，无法采集指纹"}, status=status.HTTP_403_FORBIDDEN)
        correct_person = None
        for person in obj.person.all():
            _figure = person.worker.figures.all()
            if len(_figure) == 0:
                continue
            else:
                for single_figure in _figure:
                    if exam_equal_figure(single_figure.modal, figure_data):
                        correct_person = person
                        break
        if correct_person:
            if correct_person.checked:
                return Response(data={'error': '该人员已登陆过，请不要采集两次指纹'}, status=status.HTTP_400_BAD_REQUEST)
            correct_person.checked = datetime.datetime.now()
            correct_person.save()
            ser = AttentionsDetailSer(obj.person.all(), many=True)
            return Response(data={'people': correct_person.worker.name,
                                  'all': ser.data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(data={'error': '未找到相关指纹信息'}, status=status.HTTP_404_NOT_FOUND)


class LockCallOverPerson(APIView):
    permission_classes = (OnlyOwnerDepartmentCanRead,)

    def post(self, request: Request, *args, **kwargs):
        number = request.POST.get('number')
        try:
            attention_table = AttentionTable.objects.get(pk=number)
        except Exception:
            return Response(data={'error': '未找到相关出勤表信息'}, status=status.HTTP_404_NOT_FOUND)
        if attention_table.lock:
            return Response(data={'detail': '表已锁定，请不要重复操作，可以开始点名'}, status=status.HTTP_200_OK)
        attention_table.lock = True
        attention_table.save()
        return Response(status=status.HTTP_201_CREATED)


class GetWorkerCanAdd(APIView):
    '''
    返回可以向该点名表中添加的人员列表，超级管理员无法使用
    '''

    def get(self, request: Request, id, *args, **kwargs):
        number = id
        try:
            attention_table = AttentionTable.objects.get(pk=number)
        except Exception:
            return Response(data={'error': '未找到相关出勤表信息'}, status=status.HTTP_404_NOT_FOUND)
        if attention_table.lock:
            return Response(data={'detail': '表已锁定，请不要重复操作，可以开始点名'}, status=status.HTTP_200_OK)
        workers = Worker.objects.filter(position__department=request.user.user.department)
        had_attention = attention_table.person.all()
        for worker in had_attention:
            workers.exclude(pk=worker.pk)
        return Response(data=WorkerSer(workers, many=True).data, status=status.HTTP_200_OK)


@api_view(['POST'])
def call_over_note(request, id):
    if not request.user.is_authenticated():
        return Response(data={'error': 'login required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        call_over = CallOverDetail.objects.get(pk=id)
    except:
        return Response(data={'error': '未找到相关点名表信息'}, status=status.HTTP_404_NOT_FOUND)
    if call_over.department == request.user.user.department:
        data = request.data.get('data', '')
        print(data)
        call_over.note = data
        call_over.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(data={'error': 'no permission'}, status=status.HTTP_400_BAD_REQUEST)
