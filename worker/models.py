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

    def __str__(self):
        return '{}的{}指纹'.format(self.worker_set.first().name, self.name)


class FigureSetting(models.Model):
    # 控制部门是否可以采集或变更指纹的行为
    department = models.OneToOneField('base.Department', verbose_name='部门')
    can_add = models.BooleanField(default=False, verbose_name='可增加')
    can_delete = models.BooleanField(default=False, verbose_name='可删除')

    class Meta:
        verbose_name_plural = '部门权限设定'
        verbose_name = '部门权限'

    def __str__(self):
        return self.department.name


class Position(models.Model):
    name = models.CharField(max_length=15, verbose_name='名称')
    department = models.ForeignKey('base.Department', verbose_name='部门')
    number = models.PositiveSmallIntegerField(verbose_name='定员数')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'department')
        verbose_name_plural = '职位'
        verbose_name = '职位'


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

    def __str__(self):
        return '{}-{}-{} {}的{}'.format(self.date.year, self.date.month, self.date.day, self.department.name,
                                       '白班' if self.day_number == '1' else '夜班')


class AttentionDetail(models.Model):
    worker = models.ForeignKey('worker.Worker')
    position = models.ForeignKey('worker.Position')
    study = models.BooleanField(default=False, verbose_name='是否为学员')
    checked = models.DateTimeField(blank=True, null=True, verbose_name='签到时间')
    raw_string = models.TextField(blank=True, null=True, verbose_name='指纹仪模板')

    def __str__(self):
        return self.worker.name
