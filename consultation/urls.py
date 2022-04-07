from django.urls import path, include
from rest_framework.routers import DefaultRouter
from consultation.views import ConsultationViewSet

router = DefaultRouter()
router.register(r'', ConsultationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
