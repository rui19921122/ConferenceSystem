from rest_framework import serializers

from . import models


class ClassPlanBase(serializers.HyperlinkedModelSerializer):
    edit_url = serializers.HyperlinkedIdentityField(view_name='class-plan-base-detail')

    class Meta:
        model = models.ClassPlanBase
        fields = ('number', 'name', 'edit_url')


class ClassPlanPublishDetail(serializers.ModelSerializer):
    class Meta:
        model = models.SinglePublishDetail
        fields = ('number', 'detail')


class ClassPlanDayDetail(serializers.ModelSerializer):
    publish_detail = ClassPlanPublishDetail(many=True)

    class Meta:
        model = models.ClassPlanDayDetail
        fields = ('number', 'department', 'style', 'publish_detail')


class ClassPlanDayTable(serializers.ModelSerializer):
    day_detail = ClassPlanDayDetail(many=True)

    class Meta:
        model = models.ClassPlanDayTable
        fields = ('publish_person', 'publish_time', 'time', 'day_detail')

    def create(self, validated_data):
        day_detail = validated_data.pop('day_detail')
        day_table = models.ClassPlanDayTable.objects.create(**validated_data)
        for single_detail in day_detail:
            publish_detail = day_detail.pop('publish_detail')
            new_day_detail = models.ClassPlanDayDetail.objects.create(table=day_table,
                                                                      number=single_detail.number,
                                                                      department=single_detail.department,
                                                                      style=models.ClassPlanBase.objects.get_or_create(
                                                                          name=single_detail.style)[0])
            for single_publish_detail in publish_detail:
                models.SinglePublishDetail.objects.create(
                    detail=single_publish_detail.detail,
                    number=single_publish_detail.number,
                    parent=publish_detail
                )

        return day_table
