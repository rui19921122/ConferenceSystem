import datetime
from rest_framework import serializers
from . import models


class WorkSerializetion(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    position = serializers.StringRelatedField()

    class Meta:
        model = models.Worker
        fields = '__all__'
