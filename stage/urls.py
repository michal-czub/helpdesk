from django.urls import path, include
from stage import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', views.StageViewSet)

urlpatterns = [
    path('', include(router.urls))
]
