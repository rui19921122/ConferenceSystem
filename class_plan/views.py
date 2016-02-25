import datetime

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from . import models, serialzation
from .permissions import IsAllowedOrReadOnly


class ClassPlanDetailViewSet(ModelViewSet):
    permission_classes = (IsAllowedOrReadOnly,)
    queryset = models.ClassPlanDayDetail.objects.all()
    serializer_class = (serialzation.ClassPlanPublishDetail,)


class ClassPlanBaseViewSet(ModelViewSet):
    permission_classes = (IsAllowedOrReadOnly,)
    queryset = models.ClassPlanBase.objects.all()
    serializer_class = (serialzation.ClassPlanBase)


class ClassPlan(APIView):
    permission_classes = (IsAllowedOrReadOnly,)

    def post(self, request):
        user = request.user
        data = request.data
        data.update({'publish_person': user.pk})
        serialzation_data = serialzation.ClassPlanDayTable(data=data)
        if serialzation_data.is_valid():
            serialzation_data.save()
            return Response(serialzation_data.data, status=status.HTTP_201_CREATED)
        else:
            print(serialzation_data.errors)


class ClassPlanByDate(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ClassPlanDayTable.objects.all()
    permission_classes = (IsAllowedOrReadOnly,)
    serializer_class = serialzation.ClassPlanDayTable
    lookup_field = 'time'
    lookup_url_kwarg = 'date'

    def put(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        date = kwargs['date'].split('-')
        data.update({'publish_person': user.pk})
        try:
            queryset = self.get_queryset().get(time=data.get('time'))
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if datetime.date(int(date[0]), int(date[1]), int(date[2])) != queryset.time:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serialzation_data = serialzation.ClassPlanDayTable(data=data)
        if serialzation_data.is_valid():
            queryset.delete()
            serialzation_data.save()
            return Response(serialzation_data.data, status=status.HTTP_200_OK)
        else:
            return Response(serialzation_data.errors, status=status.HTTP_400_BAD_REQUEST)
