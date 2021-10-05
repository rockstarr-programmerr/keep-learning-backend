from rest_framework.viewsets import ModelViewSet

from classroom.filters import ReadingExerciseFilter
from classroom.models import ReadingExercise
from classroom.permissions import IsTeacherOwnsExercise
from classroom.serializers import ReadingExerciseSerializer


class ReadingExerciseViewSet(ModelViewSet):
    queryset = ReadingExercise.objects.all()
    serializer_class = ReadingExerciseSerializer
    filterset_class = ReadingExerciseFilter
    permission_classes = [IsTeacherOwnsExercise]
    ordering_fields = ['identifier']
    ordering = ['identifier']
