from rest_framework import serializers
from .models import ScrapyData, StationUserAndPassword


class ScrapySer(serializers.ModelSerializer):
    class Meta:
        model = ScrapyData
        fields = '__all__'


class PasswordSer(serializers.ModelSerializer):
    class Meta:
        model = StationUserAndPassword
        fields = '__all__'
