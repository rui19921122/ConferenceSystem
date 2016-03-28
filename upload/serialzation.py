from rest_framework import serializers
from call_over.models import Photos
from drf_extra_fields.fields import Base64ImageField


class FileUpload(serializers.ModelSerializer):
    image = Base64ImageField(required=True)

    class Meta:
        model = Photos
        fields = '__all__'
