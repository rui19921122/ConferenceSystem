from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class CallOverDetail(models.Model):
    department = models.ForeignKey('base.Department')
    host_person = models.ForeignKey(User)
    attend_person_unused = models.ManyToManyField('worker.Worker', related_name='unused_worker')
    attend_person_used = models.ManyToManyField('worker.Worker', related_name='used_worker')
    begin_time = models.TimeField(auto_now_add=True)
    end_time = models.TimeField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    class_number = models.SmallIntegerField(choices=(
        (1, 1), (2, 2), (3, 3), (4, 4)
    ))
    day_number = models.SmallIntegerField(choices=(
        (1, '白班'), (2, '夜班')
    ))


class Photos(models.Model):
    image = models.ImageField(upload_to='CallOverImage')
    date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(CallOverDetail)


class Audios(models.Model):
    audio = models.FileField(upload_to='CallOverAudio')
    date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(CallOverDetail)


class CallOverNumber(models.Model):
    date = models.DateField()
    day_number = models.SmallIntegerField(choices=(
        (1, '白班'), (2, '夜班')
    ))
    class_number = models.SmallIntegerField(choices=(
        (1, 1), (2, 2), (3, 3), (4, 4)
    ))

    class Meta:
        unique_together = (('date', 'day_number'),)
