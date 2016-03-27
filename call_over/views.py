import datetime

from django.http import request
from django.db.models import Q
from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .serialzation import CallOverDetailSer, PhotoSer, AudioSer, WorkerSer, CallOverSer
from .models import CallOverDetail
from professionalStudy.models import ProfessionalStudy
from accidentCase.models import Accident
from class_plan.models import ClassPlanDayTable
from class_plan.serialzation import ClassPlanDayTable as ClassPlanDayTableSer
from accidentCase.serization import AccidentSerializer
from professionalStudy.serialzation import ProfessionalStudySerializer
from .models import CallOverNumber
from .permission import OnlyOwnerDepartmentCanRead

import time


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
        today = datetime.datetime.today()
        number = str(request.data.get('number'))
        query = mapNumberToQuery[number]
        unused = request.data.get('unused')
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
            for person in unused:
                new.attend_person_unused.add(person)
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

    def list(self, request: request.HttpRequest, *args, **kwargs):
        begin_time = request.GET.get('start', default=datetime.date.today())
        end_time = request.GET.get('end', default=datetime.date.today())
        if request.user.is_superuser:
            obj = CallOverDetail.objects.filter(date__lte=end_time, date__gte=begin_time)
        else:
            obj = CallOverDetail.objects.filter(department=request.user.user.department,
                                                date__lte=end_time,
                                                date__gte=begin_time)
        return Response(data=CallOverSer(obj, many=True).data,status=status.HTTP_200_OK)
