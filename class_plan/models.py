from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.

class ClassPlanBase(models.Model):
    name = models.CharField(max_length=50)
    number = models.PositiveSmallIntegerField(unique=True)


class DayTable(models.Model):
    publish_person = models.ForeignKey('base.Person')
    publish_time = models.DateTimeField(auto_now_add=True)
    time = models.DateField()

    def save(self, *args, **kwargs):
        if self.publish_person.department.name == '调度车间':
            super(DayTable, self).save(*args, **kwargs)
        else:
            raise ValidationError("提交人不为调度车间管理人员")


class DayDetail(models.Model):
    table = models.ForeignKey(DayTable)
    department = models.CharField(max_length=100)
    style = models.ForeignKey(ClassPlanBase)


class SinglePublishDetail(models.Model):
    father_detail = models.ForeignKey(DayDetail)
    content = models.CharField(max_length=500)
    number = models.PositiveSmallIntegerField()


class SingleClaimDetail(models.Model):
    father_detail = models.ForeignKey(DayDetail)
    content = models.CharField(max_length=500)
    number = models.PositiveSmallIntegerField()
    department = models.ForeignKey('base.Department')
    claim_time = models.DateTimeField(auto_now_add=True)


class WhichDepartmentCanEditClassPlan(models.Model):
    """
    指定谁可以更改班计划,超级管理员一直具有权限
    """
    department = models.OneToOneField('base.Department', )
