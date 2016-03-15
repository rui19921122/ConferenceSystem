from django.db.models import Q
from django.shortcuts import render
from .models import Accident
from .serization import AccidentSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView


# Create your views here.
class AccidentView(ListCreateAPIView):
    queryset = Accident.objects.all()
    serializer_class = AccidentSerializer

    def perform_create(self, serializer):
        user = self.request.user
        department = user.user.department
        serializer.save(publish_person=user, department=department)


class AccidentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Accident.objects.all()
    serializer_class = AccidentSerializer


class GetUnlearnedAccident(ListAPIView):
    serializer_class = AccidentSerializer

    def get_queryset(self):
        department = self.request.user.user.department
        return Accident. \
            objects.filter(Q(department=department),
                           Q(checked_by_first__isnull=True)
                           | Q(checked_by_second__isnull=True)
                           | Q(checked_by_third__isnull=True)
                           | Q(checked_by_forth__isnull=True))
