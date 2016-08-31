import datetime

import xlrd
from django.core.files import File
from django.http.response import HttpResponse
from django.views import generic
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import FileUploadParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
import json

from accidentCase.models import Accident, AccidentFiles
from call_over.models import Audios, Photos
from call_over.models import CallOverDetail
from class_plan.models import ClassPlanDayDetail, ClassPlanBase, ClassPlanDayTable, SinglePublishDetail
from class_plan.models import WhichDepartmentCanEditClassPlan
from utils.response import ErrorResponse
from worker.models import AttentionTable
from . import serialzation
from .models import ClassPlanUpload


# Create your views here.

def handleClassPlanFile(request, date):
    if request.method == 'POST' and request.user.is_authenticated():
        if not WhichDepartmentCanEditClassPlan.objects.filter(
                department=request.user.user.department).exists():
            return HttpResponse(content=json.dumps({'error': '没有修改权限', 'status': 'error'}),
                                status=status.HTTP_403_FORBIDDEN)
        date = date.split('-')
        _date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
        if ClassPlanDayTable.objects.filter(time=_date).exists():  # 判定班计划表是否已经锁定
            if ClassPlanDayTable.objects.get(time=_date).lock:
                return HttpResponse(content=json.dumps({'error': 'locked', 'status': 'error'}),
                                    status=status.HTTP_403_FORBIDDEN)
            else:
                ClassPlanDayTable.objects.get(time=_date).delete()
        new = ClassPlanUpload(person=request.user, file=request.FILES['file'])
        new.save()
        try:
            excel = xlrd.open_workbook(new.file.path, formatting_info=True)
        except:
            return HttpResponse(content=json.dumps({'error': 'wrong format', 'status': 'error'}),
                                status=status.HTTP_403_FORBIDDEN)
        sheet = excel.sheet_by_index(0)
        if ClassPlanDayTable.objects.filter(time=_date).exists():
            ClassPlanDayTable.objects.get(time=_date).delete()
        table = ClassPlanDayTable.objects.create(publish_person=request.user, time=_date)
        print(sheet.merged_cells)
        for merged in sheet.merged_cells:
            first_row, last_row, first_col, last_col = merged
            number = sheet.cell_value(first_row, 0)
            name = sheet.cell_value(first_row, 1)
            department = sheet.cell_value(first_row, 3)
            new_day_detail = ClassPlanDayDetail(
                department=department, number=number,
                style=ClassPlanBase.objects.get_or_create(name=name,
                                                          )[0],
                table=table
            )
            new_day_detail.save()
            if first_col != 0:
                continue
            for row in range(first_row, last_row):
                SinglePublishDetail.objects.create(detail=sheet.cell_value(row, 2), parent=new_day_detail)
        return HttpResponse(content=json.dumps({'status': 'success'}), status=201)


def handleUploadImage(request, id):
    if request.user.is_authenticated() and request.method == 'POST':
        department = request.user.user.department
        detail = CallOverDetail.objects.get(pk=id)
        if detail.department == detail.department:
            file = request.FILES['file']
            new = Photos(image=file, parent_id=detail.pk)
            new.save()
            return HttpResponse(status=status.HTTP_201_CREATED)


# class handleUploadImage(generic.View):
#     def post(self, request: Request, id):
#         user = request.user
#         if user.is_authenticated():
#             department = user.user.department
#             detail = CallOverDetail.objects.get(pk=id)
#             if detail.department == department:
#                 data = request.data
#                 data['parent'] = id
#                 ser = serialzation.FileUpload(data=data)
#                 if ser.is_valid():
#                     ser.save()
#                     return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
def handleUploadAudio(request, id):
    if not request.user.is_authenticated():
        return HttpResponse(status=status.HTTP_403_FORBIDDEN)
    user = request.user
    department = user.user.department
    try:
        detail = AttentionTable.objects.get(pk=id)
    except:
        return ErrorResponse("not found")
    # if Audios.objects.filter(parent_id=id).exists():
    #     return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    with open('{}-{}-{}.avi'.format(
            department.name, detail.date, detail.day_number
    ), 'wb+') as file:
        new_file = File(file)
        new_file.write(request.body)
        new = Audios(audio=new_file, attend_table_id=id)
        new.save()

    return Response(data={'status': 'success'}, status=status.HTTP_201_CREATED)


def handleUploadAccident(request, id):
    if request.method != 'POST':
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    if not request.user.is_authenticated():
        return HttpResponse(status=status.HTTP_403_FORBIDDEN)
    user = request.user
    department = user.user.department
    accident_case = Accident.objects.get(pk=id)
    if not accident_case.department_id == department.id:
        return HttpResponse(status=status.HTTP_403_FORBIDDEN)
    accident_case.files.add(AccidentFiles.objects.create(file=request.FILES['file'], filename=request.FILES[
        'file'].name))
    return HttpResponse(status=status.HTTP_201_CREATED)


def deleteUploadAccident(request, id):
    if request.method != 'DELETE':
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    if not request.user.is_authenticated():
        return HttpResponse(status=status.HTTP_403_FORBIDDEN)
    user = request.user
    department = user.user.department
    file = AccidentFiles.objects.get(pk=id)
    accident = Accident.objects.get(files__exact=file)
    if accident.department == department:
        file.delete()
        return HttpResponse(status=status.HTTP_202_ACCEPTED)
    else:
        return HttpResponse(status=status.HTTP_403_FORBIDDEN)
