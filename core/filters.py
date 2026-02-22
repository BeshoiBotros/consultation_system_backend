import django_filters
from patients.models import Patient
from consultations.models import Consultation

class PatientFilter(django_filters.FilterSet):
    
    full_name = django_filters.CharFilter(field_name='full_name', lookup_expr='icontains')
    date_of_birth_from = django_filters.DateFilter(field_name='date_of_birth', lookup_expr='gte')
    date_of_birth_to = django_filters.DateFilter(field_name='date_of_birth', lookup_expr='lte')
    email = django_filters.CharFilter(field_name='email', lookup_expr='iexact')
    
    class Meta:
        model = Patient
        fields = '__all__'

class ConsultationFilter(django_filters.FilterSet):

    patient_id = django_filters.UUIDFilter(field_name='patient')
    created_at_from = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_at_to = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Consultation
        exclude = ['ai_summary']
        