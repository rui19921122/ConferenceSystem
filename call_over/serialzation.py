import datetime

from rest_framework import serializers
from rest_framework.relations import RelatedField

from class_plan.serialzation import ClassPlanDayTable
from professionalStudy.serialzation import ProfessionalStudySerializer
from worker.models import Worker
from .models import Photos, Audios, CallOverDetail
from accidentCase.serization import AccidentSerializer


class SlugUserNameRelatedField(RelatedField):
    def to_representation(self, value):
        return value.user.name


class CallOverSer(serializers.ModelSerializer):
    attend_person_used = serializers.SlugRelatedField(many=True,
                                                      slug_field='name',
                                                      read_only=True)
    attend_person_unused = serializers.SlugRelatedField(many=True,
                                                        slug_field='name',
                                                        read_only=True)
    department = serializers.SlugRelatedField(slug_field='name', read_only=True)
    host_person = SlugUserNameRelatedField(read_only=True)

    class Meta:
        model = CallOverDetail
        fields = '__all__'


class CallOverDetailSer(serializers.Serializer):
    class_plan = ClassPlanDayTable(read_only=True, required=False)
    study = ProfessionalStudySerializer(many=True, read_only=True, required=False)
    accident = AccidentSerializer(many=True, read_only=True, required=False)


class PhotoSer(serializers.ModelSerializer):
    class Meta:
        model = Photos
        fields = ('__all__')


class AudioSer(serializers.ModelSerializer):
    class Meta:
        model = Audios
        fields = ('audio', 'date')


class CallOverQueryDetailSer(serializers.Serializer):
    data = CallOverDetailSer()
    begin = serializers.DateTimeField()
    end = serializers.DateTimeField()
    used = serializers.ListField()
    unused = serializers.ListField()
    photo = PhotoSer(required=False, many=True)
    video = AudioSer(required=False, many=True)


class WorkerSer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = '__all__'
