from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class ClassPlanBase(models.Model):
    name = models.CharField(max_length=50)


class ClassPlanDayTable(models.Model):
    publish_person = models.ForeignKey(User)
    publish_time = models.DateTimeField(auto_now_add=True)
    time = models.DateField()


class ClassPlanDayDetail(models.Model):
    table = models.ForeignKey('class_plan.ClassPlanDayTable',
                              related_name='day_detail', )
    department = models.CharField(max_length=100)
    style = models.ForeignKey('class_plan.ClassPlanBase', )
    number = models.PositiveSmallIntegerField()


class SinglePublishDetail(models.Model):
    detail = models.CharField(max_length=500)
    parent = models.ForeignKey('class_plan.ClassPlanDayDetail', related_name='publish_detail')


class SingleClaimDetail(models.Model):
    father_detail = models.ForeignKey('class_plan.SinglePublishDetail')
    content = models.CharField(max_length=500)
    number = models.PositiveSmallIntegerField()
    department = models.ForeignKey('base.Department')
    claim_time = models.DateTimeField(auto_now_add=True)


class WhichDepartmentCanEditClassPlan(models.Model):
    """
    指定谁可以更改班计划,超级管理员一直具有权限
    """
    department = models.OneToOneField('base.Department')
