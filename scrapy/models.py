from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class StationUserAndPassword(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=50)
    password = models.CharField(verbose_name='密码', max_length=50)
    user = models.OneToOneField(User)

    class Meta:
        verbose_name = '路局系统用户名密码存储'


class ScrapyData(models.Model):
    title = models.CharField(verbose_name='标题', max_length=50)
    content = models.TextField(verbose_name='内容')
    number = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['-number', ]
