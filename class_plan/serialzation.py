import datetime

from rest_framework import serializers

from . import models


class ClassPlanBase(serializers.HyperlinkedModelSerializer):
    edit_url = serializers.HyperlinkedIdentityField(view_name='class-plan-base-detail')

    class Meta:
        model = models.ClassPlanBase
        fields = ('name', 'edit_url')


class ClassPlanPublishDetail(serializers.ModelSerializer):
    # todo 添加返回直接编辑链接的选项

    class Meta:
        model = models.SinglePublishDetail
        fields = ('detail', 'id')


class ClassPlanDayDetailSerializer(serializers.ModelSerializer):
    publish_detail = ClassPlanPublishDetail(many=True)
    style = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = models.ClassPlanDayDetail
        fields = ('number', 'department', 'style', 'publish_detail')


class ClassPlanDayTable(serializers.ModelSerializer):
    day_detail = ClassPlanDayDetailSerializer(many=True)

    class Meta:
        model = models.ClassPlanDayTable
        fields = ('publish_person', 'publish_time', 'time', 'day_detail', 'lock')

    def create(self, validated_data):
        day_detail = validated_data.pop('day_detail')
        day_table = models.ClassPlanDayTable.objects.create(publish_person=validated_data.get('publish_person'),
                                                            time=validated_data.get('time'))
        for single_detail in day_detail:
            publish_detail = single_detail.pop('publish_detail')
            new_day_detail = models.ClassPlanDayDetail.objects.create(table=day_table,
                                                                      number=single_detail.get('number'),
                                                                      department=single_detail.get('department'),
                                                                      style=single_detail.get('style'))
            for single_publish_detail in publish_detail:
                models.SinglePublishDetail.objects.create(
                    detail=single_publish_detail.get('detail'),
                    number=single_publish_detail.get('number'),
                    parent=new_day_detail
                )

        return day_table
