from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from core.filters import PatientFilter
from . import serializers
from . import models
from rest_framework.permissions import IsAuthenticated


class PatientViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = PatientFilter
    serializer_class = serializers.PatientSerializers
    queryset = models.Patient.objects.all()
