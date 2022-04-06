from django.urls import path, include
from rest_framework.routers import DefaultRouter
from event.views import (StaffEventViewSet, ClientEventViewSet)

router = DefaultRouter()
router.register(r'', StaffEventViewSet)

urlpatterns = [
    path('create/', ClientEventViewSet.as_view({'post': 'create'})),
    path('', include(router.urls)),
]