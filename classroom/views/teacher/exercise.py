from rest_framework.viewsets import ModelViewSet

from classroom.filters.teacher import ReadingExerciseTeacherFilter
from classroom.models import ReadingExercise
from classroom.permissions import IsTeacherOwnsExercise
from classroom.serializers.teacher import ReadingExerciseSerializer


class ReadingExerciseTeacherViewSet(ModelViewSet):
    queryset = ReadingExercise.objects.all()
    serializer_class = ReadingExerciseSerializer
    filterset_class = ReadingExerciseTeacherFilter
    permission_classes = [IsTeacherOwnsExercise]
    ordering_fields = ['identifier']
    ordering = ['identifier']
