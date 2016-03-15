from rest_framework import serializers

from . import models


class ProfessionalStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProfessionalStudy
        fields = '__all__'
        read_only_fields = ['department', 'publish_person']
