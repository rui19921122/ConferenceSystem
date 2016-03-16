import datetime

from rest_framework import serializers
from class_plan.serialzation import ClassPlanDayTable
from professionalStudy.serialzation import ProfessionalStudySerializer
from accidentCase.serization import AccidentSerializer


class CallOverDetail(serializers.BaseSerializer):
    class_plan = ClassPlanDayTable()
    study = ProfessionalStudySerializer(many=True)
    accident = AccidentSerializer(many=True)
