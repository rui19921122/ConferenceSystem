from django.shortcuts import render
from django.db.models import Q, F
from rest_framework.views import APIView
from rest_framework import generics, mixins
from . import models, serialzation
from .permission import OnlyOwnerDepartmentCanEdit
import datetime, time


# Create your views here.
class ProfessionalStudy(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    queryset = models.ProfessionalStudy.objects.all()
    serializer_class = serialzation.ProfessionalStudySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        department = self.request.user.user.department
        publish_person = self.request.user
        serializer.save(department=department, publish_person=publish_person)


class ProfessionalStudyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProfessionalStudy.objects.all()
    serializer_class = serialzation.ProfessionalStudySerializer
    permission_classes = (OnlyOwnerDepartmentCanEdit,)


class ProfessionalStudyPostStudy(APIView):
    def post(self, request):
        user = request.user
        now = time.time()


class GetUnlearnedStudy(generics.ListAPIView):
    serializer_class = serialzation.ProfessionalStudySerializer

    def get_queryset(self):
        department = self.request.user.user.department
        return models.ProfessionalStudy. \
            objects.filter(Q(department=department),
                           Q(checked_by_first__isnull=True)
                           | Q(checked_by_second__isnull=True)
                           | Q(checked_by_third__isnull=True)
                           | Q(checked_by_forth__isnull=True))
