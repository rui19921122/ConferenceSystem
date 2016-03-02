from rest_framework import serializers

from . import models


class ProfessionalStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProfessionalStudy
        fields = ('publish_time', 'publish_person', 'content', 'department',
                  'checked_by_first', 'checked_by_second', 'checked_by_third', 'checked_by_forth')
        read_only_fields = ('publish_time', 'publish_person', 'department',
                            'checked_by_first', 'checked_by_second', 'checked_by_third', 'checked_by_forth')
