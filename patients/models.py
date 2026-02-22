from django.db import models
import uuid
from core.models import SoftDeleteModel

class Patient(SoftDeleteModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    email = models.EmailField()
