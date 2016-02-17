from django.db import models


# Create your models here.
class CheckIn(models.Model):
    json = models.ManyToManyField('worker.Worker')
    date = models.DateField()
    class_number = models.CharField(max_length=1, choices=(
        ('1', '第一班'),
        ('2', '第二班')))
    confirm_people = models.ForeignKey('base.Person')
