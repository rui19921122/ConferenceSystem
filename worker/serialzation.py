import datetime
from rest_framework import serializers
from . import models


class WorkerSerial(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class_number = serializers.IntegerField(allow_null=True)

    class Meta:
        model = models.Worker
        fields = '__all__'


class PositionSerial(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Position
        fields = ('id', 'name', 'number')
