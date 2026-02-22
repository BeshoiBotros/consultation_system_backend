from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConsultationViewSet, GenerateSummaryView

router = DefaultRouter()
router.register(r'', ConsultationViewSet, basename='consultation')

urlpatterns = [
    path('', include(router.urls)),
    path('generate-summary/<uuid:pk>/', GenerateSummaryView.as_view(), name='generate-ai-summary')
]
