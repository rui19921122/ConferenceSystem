from django.db import models


# Create your models here.
class Worker(models.Model):
    name = models.CharField(max_length=15, verbose_name='姓名', unique=True)
    position = models.ForeignKey('worker.Position')
    is_study = models.BooleanField(default=False)
    alter = models.BooleanField(default=False)
    class_number = models.PositiveSmallIntegerField(null=True, blank=True)
    figures = models.ManyToManyField('worker.Figure', verbose_name='指纹库')


class Figure(models.Model):
    modal = models.CharField(max_length=513, verbose_name='指纹模型')
    weight = models.PositiveSmallIntegerField(null=True, verbose_name='习惯权重')

    class Meta:
        ordering = ('weight',)


class Position(models.Model):
    name = models.CharField(max_length=15)
    department = models.ForeignKey('base.Department')
    number = models.PositiveSmallIntegerField(default=1)


class AttentionTable(models.Model):
    department = models.ForeignKey('base.Department')
    date = models.DateField()
    day_number = models.CharField(max_length=1,
                                  choices=(('1', '白班'), ('2', '夜班'))
                                  )
    person = models.ManyToManyField('worker.AttentionDetail')
    lock = models.BooleanField(default=False)

    class Meta:
        unique_together = ('department', 'date', 'day_number')


class AttentionDetail(models.Model):
    worker = models.ForeignKey('worker.Worker')
    position = models.ForeignKey('worker.Position')
    study = models.BooleanField(default=False, verbose_name='是否为学员')
    checked = models.DateTimeField(blank=True, null=True, verbose_name='签到时间')
    raw_string = models.TextField(blank=True, null=True, verbose_name='指纹仪模板')
