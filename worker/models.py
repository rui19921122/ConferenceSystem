from django.db import models


# Create your models here.
class Worker(models.Model):
    name = models.CharField(max_length=15, verbose_name='姓名', unique=True)
    position = models.ForeignKey('worker.Position')
    is_study = models.BooleanField(default=False)
    class_number = models.PositiveSmallIntegerField(null=True, blank=True, choices=(
        (0, '替班'),
        (1, '一班'),
        (2, '二班'),
        (3, '三班'),
        (4, '四班'),
    ))
    figures = models.ManyToManyField('worker.Figure', verbose_name='指纹库', blank=True, editable=False)

    def __str__(self):
        return self.name


class Figure(models.Model):
    modal = models.CharField(max_length=513, verbose_name='指纹模型')
    weight = models.PositiveSmallIntegerField(null=True, verbose_name='习惯权重')
    name = models.CharField(max_length=5, choices=(
        ('左手大拇指', '左手大拇指'),
        ('左手食指', '左手食指'),
        ('左手中指', '左手中指'),
        ('左手无名指', '左手无名指'),
        ('左手小拇指', '左手小拇指'),
        ('右手大拇指', '右手大拇指'),
        ('右手食指', '右手食指'),
        ('右手中指', '右手中指'),
        ('右手无名指', '右手无名指'),
        ('右手小拇指', '右手小拇指'),
    ))

    class Meta:
        ordering = ('weight',)


class FigureSetting(models.Model):
    # 控制部门是否可以采集或变更指纹的行为
    department = models.OneToOneField('base.Department')
    can_add = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)


class Position(models.Model):
    name = models.CharField(max_length=15)
    department = models.ForeignKey('base.Department')
    number = models.PositiveSmallIntegerField(verbose_name='定员数')

    class Meta:
        unique_together = ('name', 'department')


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
