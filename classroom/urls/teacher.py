from rest_framework.routers import DefaultRouter

from classroom.views import teacher as teacher_views


# NOTE: DRF has bug involve app's namespace and viewset's extra_actions,
# so we can't use app namespace for now
# Ref: https://github.com/encode/django-rest-framework/discussions/7816

urlpatterns = []

router = DefaultRouter()
router.register('classrooms', teacher_views.ClassroomTeacherViewSet, basename='classroom-teacher')
router.register('reading-exercises', teacher_views.ReadingExerciseTeacherViewSet, basename='reading-exercise-teacher')

urlpatterns.extend(router.urls)
