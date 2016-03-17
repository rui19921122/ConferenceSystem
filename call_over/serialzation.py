import datetime

from rest_framework import serializers
from class_plan.serialzation import ClassPlanDayTable
from professionalStudy.serialzation import ProfessionalStudySerializer
from accidentCase.serization import AccidentSerializer


class CallOverDetailSer(serializers.Serializer):
    class_plan = ClassPlanDayTable(read_only=True, required=False)
    study = ProfessionalStudySerializer(many=True, read_only=True, required=False)
    accident = AccidentSerializer(many=True, read_only=True, required=False)
