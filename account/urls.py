from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter

from . import views


# NOTE: DRF has bug involve app's namespace and viewset's extra_actions,
# so we can't use app namespace for now
# Ref: https://github.com/encode/django-rest-framework/discussions/7816
# app_name = 'user'

urlpatterns = [
    path('users/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='user')
router.register('me', views.MeViewSet, basename='me')
urlpatterns.extend(router.urls)
