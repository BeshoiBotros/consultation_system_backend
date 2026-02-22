from rest_framework import serializers
from . import models
from patients.serializers import PatientSerializers

class ConsultationSerializer(serializers.ModelSerializer):
    # Expose patient details on the consultation itself.
    patient_consultation = PatientSerializers(source='patient', read_only=True)

    class Meta:
        model  = models.Consultation
        fields = ['patient', 'patient_consultation', 'symptoms', 'diagnosis', 'created_at', 'ai_summary', 'id']
        extra_kwargs = {'patient': {'write_only': True}}
