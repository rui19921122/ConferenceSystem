from django.core.exceptions import ObjectDoesNotExist
from django.http.request import HttpRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serialzation, models


# Create your views here.
class UpdateClassPlanBase(APIView):
    def get_object(self, number):
        try:
            obj = models.ClassPlanBase.objects.get(number=number)
            return obj
        except ObjectDoesNotExist:
            return None

    def put(self, request, format=None):
        '''
        :type request: HttpRequest
        :rtype request: django.request.HttpRequest
        '''
        if request.user.is_superuser:
            data = serialzation.ClassPlanBase(data=request.data)
            if data.is_valid():
                instance = self.get_object(data.validated_data.get('number'))
                if instance:
                    data.update(instance=instance, validated_data=data)
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        '''
        :type request:HttpRequest
        '''
        if request.user.is_superuser:
            data = serialzation.ClassPlanBase(data=request.data)
            if data.is_valid():
                if self.get_object(number=data.validated_data.get('number')):
                    return Response(data={'errors': '冲突的序号'}, status=status.HTTP_400_BAD_REQUEST)
                data.save()
                return Response(data=data.validated_data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def get(self, request):
        '''
        :type request:HttpRequest
        '''
        if request.user.is_anonymous():
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        number = request.GET.get('number')
        if number:  # 当请求包含number时返回特定结果
            return Response(data=serialzation.ClassPlanBase(data=self.get_object(number=number)))
        return Response(status=status.HTTP_400_BAD_REQUEST)
