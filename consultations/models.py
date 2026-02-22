from django.db import models
import uuid
from patients.models import Patient
from core.models import SoftDeleteModel

class Consultation(SoftDeleteModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name='patient_consultation')

    symptoms = models.TextField(null=True, blank=True)

    diagnosis = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    ai_summary = models.JSONField(null=True, blank=True)