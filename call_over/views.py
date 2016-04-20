import ctypes
import datetime

from django.core import exceptions
from django.db.models import Q
from rest_framework import status, generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accidentCase.models import Accident
from accidentCase.serization import AccidentSerializer
from class_plan.models import ClassPlanDayTable
from class_plan.serialzation import ClassPlanDayTable as ClassPlanDayTableSer
from professionalStudy.models import ProfessionalStudy
from professionalStudy.serialzation import ProfessionalStudySerializer
from worker.models import AttentionTable, Worker, AttentionDetail
from .models import CallOverDetail
from .models import CallOverNumber
from .permission import OnlyOwnerDepartmentCanRead
from .serialzation import PhotoSer, AudioSer, WorkerSer, CallOverSer, AttentionSer, AttentionsDetailSer

windll = ctypes.windll.LoadLibrary(r'C:\Users\Administrator\Desktop\ConferenceSystem\JZTDevDll.dll')


def exam_equal_figure(source, string):
    f = windll.FPIMatch(source.encode('utf-8'), string.encode('utf-8'), 3)
    return True if f >= 0 else False


def get_current_class():
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
        print(get_current_class().class_number)
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
            locked = AttentionTable.objects.get(date=default.date, department=department, day_number=default.day_number)
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
                                                day_number=default_class_number.day_number)
            pk = new.pk
            exist = new
        else:
            exist = exist[0]
            pk = exist.pk
            try:
                class_plan = ClassPlanDayTable.objects.get(time=today)
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
    queryset = AttentionTable
    serializer_class = AttentionSer

    def list(self, request: Request, *args, **kwargs):
        default = get_current_class()
        date = request.GET.get('date', default=default.date)
        day_number = default.day_number
        class_number = default.class_number
        department = request.user.user.department
        try:
            attention_table = AttentionTable.objects.get(date=date, day_number=day_number, department=department)

        except exceptions.ObjectDoesNotExist:
            department = request.user.user.department
            workers = Worker.objects.filter(position__department=request.user.user.department,class_number=class_number)
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
        return Response(data=self.get_serializer_class()(attention_table).data, status=status.HTTP_200_OK)


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
            progress = obj.person.filter(study=False, checked__isnull=False).count() / obj.person.all().count()
            return Response(data={'people': correct_person.worker.name}, status=status.HTTP_201_CREATED)
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
