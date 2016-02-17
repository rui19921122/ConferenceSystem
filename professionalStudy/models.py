from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class ProfessionalStudy(models.Model):
    publish_time = models.DateTimeField(auto_now_add=True)
    publish_person = models.ForeignKey(User)
    content = models.TextField()
    checked_by_first = models.DateTimeField(blank=True)
    checked_by_second = models.DateTimeField(blank=True)
    checked_by_third = models.DateTimeField(blank=True)
    checked_by_forth = models.DateTimeField(blank=True)
    department = models.ForeignKey('base.Department')

    def save(self, *args, **kwargs):
        self.department = self.publish_person.person.department
        super(ProfessionalStudy, self).save(*args, **kwargs)
