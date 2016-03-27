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
    checked_by_first = models.ForeignKey('call_over.CallOverDetail', blank=True, null=True,
                                            related_name='accident_first')
    checked_by_second = models.ForeignKey('call_over.CallOverDetail', blank=True, null=True,
                                             related_name='accident_second')
    checked_by_third = models.ForeignKey('call_over.CallOverDetail', blank=True,
                                            null=True, related_name='accident_third')
    checked_by_forth = models.ForeignKey('call_over.CallOverDetail', blank=True,
                                            null=True,
                                            related_name='accident_forth')

    def study(self, number, exist):
        if number == '1':
            self.checked_by_first = exist
        if number == '2':
            self.checked_by_second = exist
        if number == '3':
            self.checked_by_third = exist
        if number == '4':
            self.checked_by_forth = exist
        self.save()
