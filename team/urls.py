from django.urls import path, include
from team.views import TeamViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', TeamViewSet)

urlpatterns = [
    path('', include(router.urls)),
]