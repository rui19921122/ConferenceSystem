from django.shortcuts import render
from django.views.generic import View
from .models import ClassPlanUpload
import datetime
from django.http.response import HttpResponse
from class_plan.models import ClassPlanDayDetail, ClassPlanBase, ClassPlanDayTable, SinglePublishDetail
import xlrd


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
