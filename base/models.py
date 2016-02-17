from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=20)
    department = models.ForeignKey('base.Department')
    user = models.OneToOneField(User)


class ProfessionalSystem(models.Model):
    name = models.CharField(max_length=20)


class Department(models.Model):
    name = models.CharField(max_length=20)
    system = models.ForeignKey('base.ProfessionalSystem')
