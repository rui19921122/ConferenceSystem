from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from base.models import Department
from utils.response import ErrorResponse
from .serialzation import CallOverDetailSer, DepartmentCanQuerySer, QueryCallOverListSer
from call_over.models import CallOverDetail
import datetime

# Create your views here.
from rest_framework.request import Request


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
        print(query_call_overs)
        print(start, end)
        ser = {
            'call_over_list': CallOverDetailSer(query_call_overs, many=True).data,
            'department_can_query': DepartmentCanQuerySer(query_departments, many=True).data
        }
        return Response(data=ser, status=200)


class GetCallOverDetail(APIView):
    def get(self, request: Request):
        pass
