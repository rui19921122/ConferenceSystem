from rest_framework import serializers

from .models import Accident, AccidentFiles


class SlugUserNameRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.user.name


class FilesSer(serializers.ModelSerializer):
    class Meta:
        model = AccidentFiles
        fields = '__all__'


class AccidentSerializer(serializers.ModelSerializer):
    publish_person = SlugUserNameRelatedField(read_only=True)
    files = FilesSer(many=True,read_only=True)

    class Meta:
        model = Accident
        fields = '__all__'
        read_only_fields = ('publish_person', 'department', 'check_by_first',
                            'check_by_second', 'check_by_third', 'check_by_forth',
                            'files')
