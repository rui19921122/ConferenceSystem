from django.db.models import Q
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from accidentCase.models import Accident
from base.models import Department
from class_plan.models import ClassPlanDayTable
from professionalStudy.models import ProfessionalStudy
from utils.response import ErrorResponse
from .serialzation import CallOverDetailSer, DepartmentCanQuerySer, CallOverDetailSerDepth3
from call_over.models import CallOverDetail, Photos, Audios
import datetime
from professionalStudy.serialzation import ProfessionalStudySerializer
from class_plan.serialzation import ClassPlanDayTable as ClassPlanDayTableSer
from accidentCase.serization import AccidentSerializer

# Create your views here.
from django.http.request import HttpRequest
from rest_framework.request import Request
from call_over.serialzation import PhotoSer, AudioSer


def parse_date(string: str):
    year, month, day = string.split('-')
    return datetime.datetime(year=int(year), month=int(month), day=int(day))


class QueryList(APIView):
    def get(self, request: Request):
        if 'start' in request.GET and 'end' in request.GET:
            try:
                start = parse_date(request.GET.get('start'))
                end = parse_date(request.GET.get('end'))
            except:
                return ErrorResponse('错误的日期格式')
        else:
            start = datetime.datetime.today() - datetime.timedelta(days=7)
            end = datetime.datetime.today()
        department = request.user.user.department
        query_departments = Department.objects.filter(is_superuser=False) if department.is_superuser else \
            Department.objects.filter(name=department.name)
        query_call_overs = CallOverDetail.objects.filter(
            date__gte=start,
            date__lte=end,
            end_time__isnull=False
        )
        ser = {
            'call_over_list': CallOverDetailSer(query_call_overs, many=True).data,
            'department_can_query': DepartmentCanQuerySer(query_departments, many=True).data
        }
        return Response(data=ser, status=200)


class QueryDetail(APIView):
    def get(self, request: HttpRequest, id):
        try:
            f = CallOverDetail.objects.get(id=id)
        except:
            return ErrorResponse('未发现符合的点名')
        if request.user.is_superuser or f.department == request.user.user.department:
            pass
        else:
            return ErrorResponse("无权限")
        try:
            audios = Audios.objects.get(parent=f)
            audios_ser = AudioSer(audios).data
        except:
            audios_ser = None
        try:
            photos = Photos.objects.filter(parent=f)
            if photos.count() == 0:
                raise ValueError
            photos_ser = PhotoSer(photos, many=True).data
        except:
            photos_ser = []
        try:
            class_plan = ClassPlanDayTable.objects.get(time=f.date)
        except:
            class_plan = None
        study = ProfessionalStudy.objects.filter(
            Q(checked_by_first=f)
            | Q(checked_by_second=f)
            | Q(checked_by_third=f)
            | Q(checked_by_forth=f)
        )
        accident = Accident.objects.filter(
            Q(checked_by_first=f)
            | Q(checked_by_second=f)
            | Q(checked_by_third=f)
            | Q(checked_by_forth=f)
        )
        class_plan_ser = ClassPlanDayTableSer(class_plan)
        study_ser = ProfessionalStudySerializer(study, many=True)
        accident_ser = AccidentSerializer(accident, many=True)
        return Response(
            data={
                'detail': CallOverDetailSerDepth3(instance=f).data,
                'photos': photos_ser,
                'audios': audios_ser,
                'study': study_ser.data,
                'accident': accident_ser.data,
                'class_plan': class_plan_ser.data
            }
        )
