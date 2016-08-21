from rest_framework import serializers
from call_over.models import CallOverDetail
from base.models import Department
from rest_framework.relations import RelatedField


class SlugUserNameRelatedField(RelatedField):
    def to_representation(self, value):
        return value.user.name


class CallOverDetailSer(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(slug_field='name', read_only=True)
    host_person = SlugUserNameRelatedField(read_only=True)

    class Meta:
        model = CallOverDetail
        fields = '__all__'


class DepartmentCanQuerySer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class QueryCallOverListSer(serializers.Serializer):
    call_over_list = CallOverDetailSer(many=True)
    department_can_query = DepartmentCanQuerySer(many=True)
