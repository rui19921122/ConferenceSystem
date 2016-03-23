import os

from PIL import Image
from django.core.files import File
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import View
from rest_framework import status
from rest_framework.response import Response
from call_over.models import Audios
from .models import ClassPlanUpload
from call_over.models import CallOverDetail
import datetime
from django.http.response import HttpResponse
from class_plan.models import ClassPlanDayDetail, ClassPlanBase, ClassPlanDayTable, SinglePublishDetail
from rest_framework.views import APIView
import base64
import xlrd
import io
from . import serialzation
import tempfile


# Create your views here.

def handleClassPlanFile(request, date):
    if request.method == 'POST' and request.user.is_authenticated():
        new = ClassPlanUpload(person=request.user, file=request.FILES['file'])
        new.save()
        excel = xlrd.open_workbook(new.file.path)
        sheet = excel.sheet_by_index(0)
        date = date.split('-')
        _date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
        if ClassPlanDayTable.objects.filter(time=_date).exists():
            ClassPlanDayTable.objects.get(time=_date).delete()
        table = ClassPlanDayTable.objects.create(publish_person=request.user, time=_date)
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
        return HttpResponse(status=201)


class handleUploadImage(APIView):
    def post(self, request, id):
        user = request.user
        if user.is_authenticated():
            department = user.user.department
            detail = CallOverDetail.objects.get(pk=id)
            if detail.department == department:
                data = request.data
                data['parent'] = id
                ser = serialzation.FileUpload(data=data)
                ser.is_valid()
                ser.save()
                return Response(status=status.HTTP_201_CREATED)


import time


def handleUploadAudio(request, id):
    if request.method != 'POST':
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    if not request.user.is_authenticated():
        return HttpResponse(status=status.HTTP_403_FORBIDDEN)
    user = request.user
    department = user.user.department
    with open('1.wav', 'wb+') as file:
        new_file = File(file)
        new_file.write(request.body)
        new = Audios(audio=new_file, parent_id=id)
        new.save()
    return HttpResponse(status=status.HTTP_201_CREATED)
