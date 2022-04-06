from django.urls import path, include
from application.views import ApplicationViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', ApplicationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
