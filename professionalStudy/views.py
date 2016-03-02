from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from . import models, serialzation
from .permission import OnlyOwnerDepartmentCanEdit
import datetime, time


# Create your views here.
class ProfessionalStudy(generics.ListCreateAPIView):
    queryset = models.ProfessionalStudy.objects.all()
    serializer_class = serialzation.ProfessionalStudySerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(
            publish_person=user,
        )


class ProfessionalStudyDetail(generics.RetrieveUpdateAPIView):
    queryset = models.ProfessionalStudy.objects.all()
    serializer_class = serialzation.ProfessionalStudySerializer
    permission_classes = (OnlyOwnerDepartmentCanEdit,)


class ProfessionalStudyPostStudy(APIView):
    def post(self, request):
        user = request.user
        now = time.time()
