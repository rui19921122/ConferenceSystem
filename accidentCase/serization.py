from rest_framework import serializers
from .models import Accident


class AccidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accident
        fields = '__all__'
        read_only_fields = ('publish_person', 'department', 'check_by_first',
                            'check_by_second', 'check_by_third', 'check_by_forth')
