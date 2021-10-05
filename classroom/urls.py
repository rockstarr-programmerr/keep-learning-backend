from rest_framework.routers import DefaultRouter

from classroom import views


# NOTE: DRF has bug involve app's namespace and viewset's extra_actions,
# so we can't use app namespace for now
# Ref: https://github.com/encode/django-rest-framework/discussions/7816

urlpatterns = []

router = DefaultRouter()
router.register('classrooms', views.ClassroomViewSet, basename='classroom')
router.register('reading-exercises', views.ReadingExerciseViewSet, basename='reading-exercise')
router.register('reading-questions', views.ReadingQuestionViewSet, basename='reading-question')

urlpatterns.extend(router.urls)
