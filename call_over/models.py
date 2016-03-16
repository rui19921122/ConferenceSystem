from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class CallOverDetail(models.Model):
    department = models.ForeignKey('base.Department')
    host_person = models.ForeignKey(User)
    attend_person_unused = models.ManyToManyField('worker.Worker', related_name='unused_worker')
    attend_person_used = models.ManyToManyField('worker.Worker', related_name='used_worker')
    begin_time = models.TimeField(auto_now_add=True)
    day = models.DateField(auto_now_add=True)
    class_number = models.SmallIntegerField(choices=(
        (1, 1), (2, 2), (3, 3), (4, 4)
    ))
