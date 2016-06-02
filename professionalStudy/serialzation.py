from rest_framework import serializers

from . import models


class SlugUserNameRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.user.name

class ProfessionalStudySerializer(serializers.ModelSerializer):
    publish_person = SlugUserNameRelatedField(read_only=True)

    class Meta:
        model = models.ProfessionalStudy
        fields = '__all__'
        read_only_fields = ['department', 'publish_person']
