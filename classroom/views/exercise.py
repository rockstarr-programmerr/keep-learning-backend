from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from classroom.filters import ReadingExerciseFilter
from classroom.models import ReadingExercise
from classroom.permissions import IsStudent, IsTeacherOrReadOnly
from classroom.serializers import (ReadingExerciseSerializer,
                                   ReadingExerciseSubmitSerializer)


class ReadingExerciseViewSet(ModelViewSet):
    queryset = ReadingExercise.objects.all()
    serializer_class = ReadingExerciseSerializer
    filterset_class = ReadingExerciseFilter
    permission_classes = [IsTeacherOrReadOnly]
    ordering_fields = ['identifier']
    ordering = ['identifier']

    @action(
        methods=['POST'], detail=True, url_path='submit-answers',
        serializer_class=ReadingExerciseSubmitSerializer,
        permission_classes=[IsStudent],
    )
    def submit_answers(self, request, pk):
        """Student submit their answer to this exercise.
        """
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        exercise = self.get_object()
        serializer.save(exercise=exercise)
        return Response()
