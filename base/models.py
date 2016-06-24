from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=20, verbose_name='姓名')
    department = models.ForeignKey('base.Department', verbose_name='部门')
    user = models.OneToOneField(User, related_name='user', verbose_name='系统内用户')

    class Meta:
        verbose_name_plural = '用户'
        verbose_name = '用户'

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=20, verbose_name='名称')
    is_superuser = models.BooleanField(default=False, verbose_name='是否可看所有')

    class Meta:
        verbose_name_plural = '部门'
        verbose_name = '部门'

    def __str__(self):
        return self.name
