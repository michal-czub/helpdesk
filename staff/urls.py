from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from staff.views import MyTokenObtainPairView, StaffRegisterView, StaffViewSet, MyAccountViewSet

router = DefaultRouter()
router.register(r'', StaffViewSet)

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('register/', StaffRegisterView.as_view(), name="register"),
    path('my/', MyAccountViewSet.as_view()),
    path('', include(router.urls)),
]