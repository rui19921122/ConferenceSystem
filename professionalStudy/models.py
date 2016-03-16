from django.db import models
from django.contrib.auth.models import User
from django.utils.datetime_safe import datetime


# Create your models here.
class ProfessionalStudy(models.Model):
    publish_time = models.DateTimeField(auto_now_add=True)
    publish_person = models.ForeignKey(User)
    content = models.TextField()
    checked_by_first = models.DateTimeField(blank=True, null=True)
    checked_by_second = models.DateTimeField(blank=True, null=True)
    checked_by_third = models.DateTimeField(blank=True, null=True)
    checked_by_forth = models.DateTimeField(blank=True, null=True)
    department = models.ForeignKey('base.Department')

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

    def save(self, *args, **kwargs):
        self.department = self.publish_person.user.department
        super(ProfessionalStudy, self).save(*args, **kwargs)
