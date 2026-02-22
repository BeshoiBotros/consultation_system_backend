from rest_framework import viewsets
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from core.filters import ConsultationFilter
from . import serializers
from . import models
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from . import tasks as consultation_tasks
from rest_framework.decorators import action

class ConsultationViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ConsultationFilter
    serializer_class = serializers.ConsultationSerializer
    queryset = models.Consultation.objects.all()

    @action(detail=True, methods=['get'])
    def summary_status(self, request, pk=None):
        consultation = self.get_object()

        if not consultation.ai_summary:
            return Response({'status': 'processing', 'detail': 'AI still generating summary...'}, status=status.HTTP_200_OK)

        return Response({'status': 'complated', 'detail': consultation.ai_summary}, status=status.HTTP_200_OK)
        
class GenerateSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        consultation = get_object_or_404(models.Consultation, pk=pk)
        consultation.ai_summary = None
        consultation.save()
        if not (consultation.diagnosis and consultation.symptoms):
            return Response({'error': 'diagonsis and symptoms must be set!'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Pass a serializable identifier to Celery (avoid EncodeError).
        consultation_tasks.generate_ai_summary_task.delay(str(consultation.pk))

        return Response({'detail': 'Ai Working pleas wait...'}, status=status.HTTP_202_ACCEPTED)
