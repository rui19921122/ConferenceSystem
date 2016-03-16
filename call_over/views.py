import datetime

from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .serialzation import CallOverDetail
from .models import CallOverDetail
from professionalStudy.models import ProfessionalStudy
from accidentCase.models import Accident
from class_plan.models import ClassPlanDayTable
import time


# Create your views here.
class GetDefaultClassNumber(APIView):
    def get(self, request):
        '''
        :param request:Request
        :return:
        '''
        user = request.user
        if user.is_authenticated():
            hour = time.localtime().tm_hour
            if hour in [7, 18, 1, 2, 3]:
                return Response({'number': 2}
                                , status=status.HTTP_200_OK)
            else:
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
        _time = time.localtime()
        if not user.is_authenticated():
            return Response(status=status.HTTP_403_FORBIDDEN)
        hour = _time.tm_hour
        today = datetime.datetime.today()
        if hour not in [7, 18, 1, 2, 3]:
            return Response('不是规定的时间段', status=status.HTTP_400_BAD_REQUEST)
        number = str(request.data.get('number'))
        query = mapNumberToQuery[number]
        unused = request.data.get('unused')
        # 处理添加相关人员
        if not CallOverDetail.objects.filter(department=department, class_number=number,
                                             day=today).exists():
            new = CallOverDetail.objects.create(department=department, host_person=user,
                                                class_number=number)
            for person in unused:
                new.attend_person_unused.add(person)

        # 处理回送数据
        all_study = []
        try:
            class_plan = ClassPlanDayTable.objects.get(time=today)
        except:
            class_plan = None
        args_edit = {'department': department, query + '__isnull': True}
        un_study = ProfessionalStudy.objects.filter(**args_edit)
        if un_study:
            for i in un_study:
                i.study(number)
        args_not_need_edit = {'department': department,
                              query + '__day': today.day,
                              query + '__month': today.month,
                              query + '__year': today.year,
                              }
        had_study = ProfessionalStudy.objects.filter(**args_not_need_edit)
        all_study = un_study + had_study
        all_accident = []
        un_accident = Accident.objects.filter(**args_edit)
        if un_accident:
            for i in un_accident:
                i.study(number)
        had_accident = Accident.objects.filter(**args_not_need_edit)
        all_accident = un_accident + had_accident
