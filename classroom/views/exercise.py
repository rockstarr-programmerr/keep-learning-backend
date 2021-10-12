from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from classroom.business.teacher import classroom as business
from classroom.filters import ReadingExerciseFilter
from classroom.models import ReadingExercise
from classroom.permissions import IsStudent, IsTeacherOrReadOnly
from classroom.serializers import (ReadingExerciseSerializer,
                                   ReadingExerciseSubmitSerializer,
                                   ReadingExerciseUploadImgSerializer)


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

    @action(
        methods=['POST'], detail=False, url_path='upload-image',
        serializer_class=ReadingExerciseUploadImgSerializer,
    )
    def upload_image(self, request):
        """Upload image used in reading exercise
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = serializer.validated_data['image']
        image_url = business.upload_reading_exercise_image(image, request=request)
        serializer = self.get_serializer(instance={'image_url': image_url})
        return Response(serializer.data)
