from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from . import models, serialzation
from .permissions import IsAllowedOrReadOnly


class ClassPlanBaseViewSet(ModelViewSet):
    permission_classes = (IsAllowedOrReadOnly,)
    queryset = models.ClassPlanBase.objects.all()
    serializer_class = (serialzation.ClassPlanBase)


class ClassPlan(generics.GenericAPIView):
    permission_classes = (IsAllowedOrReadOnly,)
