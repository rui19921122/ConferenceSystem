from django.db import models


# Create your models here.
class Worker(models.Model):
    name = models.CharField(max_length=15, verbose_name='姓名')
    position = models.ForeignKey('worker.Position')
    is_study = models.BooleanField(default=False)


class Position(models.Model):
    name = models.CharField(max_length=15)
    department = models.ForeignKey('base.Department')
    number = models.PositiveSmallIntegerField(default=1)
