from django.urls import path, include
from rest_framework.routers import DefaultRouter
from event.views import (StaffEventViewSet, ClientEventViewSet, MyEventViewSet, EventCourseViewSet)

router = DefaultRouter()
router.register(r'', StaffEventViewSet)

urlpatterns = [
    path('create/', ClientEventViewSet.as_view({'post': 'create'})),
    path('my/', MyEventViewSet.as_view({"get": "list"})),
    path('<uuid:id>/course/', EventCourseViewSet.as_view({"get": "list", "post": "create"})),
    path('', include(router.urls)),
]
