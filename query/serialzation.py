from rest_framework import serializers
from call_over.models import CallOverDetail
from base.models import Department
from rest_framework.relations import RelatedField
from worker.models import AttentionTable, AttentionDetail


class SlugUserNameRelatedField(RelatedField):
    def to_representation(self, value):
        return value.user.name


class AttentionTableSer(serializers.ModelSerializer):
    class Meta:
        model = AttentionTable
        fields = '__all__'


class CallOverDetailSer(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(slug_field='name', read_only=True)
    host_person = SlugUserNameRelatedField(read_only=True)

    class Meta:
        model = CallOverDetail
        fields = '__all__'


class AttendDetailSer(serializers.ModelSerializer):
    worker = serializers.SlugRelatedField(slug_field='name', read_only=True)
    position = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = AttentionDetail
        fields = '__all__'


class AttendTableSerSlug(serializers.ModelSerializer):
    person = AttendDetailSer(many=True, read_only=True)
    department = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = AttentionTable
        fields = '__all__'
        depth = 2


class CallOverDetailSerDepth3(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(slug_field='name', read_only=True)
    host_person = SlugUserNameRelatedField(read_only=True)
    attend_table = AttendTableSerSlug(read_only=True)

    class Meta:
        model = CallOverDetail
        fields = '__all__'
        depth = 3


class DepartmentCanQuerySer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class QueryCallOverListSer(serializers.Serializer):
    call_over_list = CallOverDetailSer(many=True)
    department_can_query = DepartmentCanQuerySer(many=True)
