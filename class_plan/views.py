from rest_framework import mixins, generics
from . import models, serialzation
from .permissions import IsAllowedOrReadOnly


class updateClassPlanBase(generics.ListCreateAPIView):
    permission_classes = (IsAllowedOrReadOnly,)
    queryset = models.ClassPlanBase.objects.all()
    serializer_class = serialzation.ClassPlanBase


class getClassPlanBaseByPk(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAllowedOrReadOnly,)
    queryset = models.ClassPlanBase.objects.all()
    serializer_class = serialzation.ClassPlanBase
