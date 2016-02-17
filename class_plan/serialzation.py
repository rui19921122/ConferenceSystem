from rest_framework import serializers
from . import models


class ClassPlanBase(serializers.ModelSerializer):
    class Meta:
        model = models.ClassPlanBase
        fields = ('number', 'name')
