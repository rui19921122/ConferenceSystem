from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied


# Create your models here.
class AccidentCase(models.Model):
    name = models.CharField(max_length=50)
    publish_person = models.ForeignKey(User)
    publish_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    relative_system = models.ManyToManyField('base.ProfessionalSystem')

    def save(self, *args, **kwargs):
        if self.publish_person.is_superuser:
            super(AccidentCase, self).save(*args, **kwargs)
        else:
            raise PermissionDenied('只有超级管理员才可以发布事故案例')


class AccidentClaim(models.Model):
    accident = models.ForeignKey('accidentCase.AccidentCase')
    department = models.ForeignKey('base.Department')
    claim_time = models.DateTimeField(auto_now_add=True)
    checked_by_first = models.DateTimeField(blank=True)
    checked_by_second = models.DateTimeField(blank=True)
    checked_by_third = models.DateTimeField(blank=True)
    checked_by_forth = models.DateTimeField(blank=True)
