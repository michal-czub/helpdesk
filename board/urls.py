from django.urls import path, include
from board.views import BoardViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', BoardViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
