from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied


# Create your models here.
from django.utils.datetime_safe import datetime


class Accident(models.Model):
    publish_person = models.ForeignKey(User)
    publish_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    department = models.ForeignKey('base.Department')
    checked_by_first = models.DateTimeField(blank=True, null=True)
    checked_by_second = models.DateTimeField(blank=True, null=True)
    checked_by_third = models.DateTimeField(blank=True, null=True)
    checked_by_forth = models.DateTimeField(blank=True, null=True)

    def study(self, number):
        ctime = datetime.now()
        if number == '1':
            self.checked_by_first = ctime
        if number == '2':
            self.checked_by_second = ctime
        if number == '3':
            self.checked_by_third = ctime
        if number == '4':
            self.checked_by_forth = ctime
        self.save()
