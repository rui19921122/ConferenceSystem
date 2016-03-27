from django.db import models
from django.contrib.auth.models import User
from django.utils.datetime_safe import datetime


# Create your models here.
class ProfessionalStudy(models.Model):
    publish_time = models.DateTimeField(auto_now_add=True)
    publish_person = models.ForeignKey(User)
    content = models.TextField()
    checked_by_first = models.ForeignKey('call_over.CallOverDetail', blank=True, null=True,
                                         related_name='study_first')
    checked_by_second = models.ForeignKey('call_over.CallOverDetail', blank=True, null=True,
                                          related_name='study_second')
    checked_by_third = models.ForeignKey('call_over.CallOverDetail', blank=True,
                                         null=True, related_name='study_third')
    checked_by_forth = models.ForeignKey('call_over.CallOverDetail', blank=True,
                                         null=True,
                                         related_name='study_forth')
    department = models.ForeignKey('base.Department')

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

    def save(self, *args, **kwargs):
        self.department = self.publish_person.user.department
        super(ProfessionalStudy, self).save(*args, **kwargs)
