from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied


# Create your models here.
class Accident(models.Model):
    name = models.CharField(max_length=50)
    publish_person = models.ForeignKey(User)
    publish_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    department = models.ForeignKey('base.Department')
    checked_by_first = models.DateTimeField(blank=True, null=True)
    checked_by_second = models.DateTimeField(blank=True, null=True)
    checked_by_third = models.DateTimeField(blank=True, null=True)
    checked_by_forth = models.DateTimeField(blank=True, null=True)
