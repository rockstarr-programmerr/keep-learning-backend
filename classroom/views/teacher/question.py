from rest_framework.viewsets import ModelViewSet

from classroom.filters.teacher import ReadingQuestionTeacherFilter
from classroom.models import ReadingQuestion
from classroom.permissions import IsTeacherOwnsQuestion
from classroom.serializers.teacher import ReadingQuestionSerializer


class ReadingQuestionTeacherViewSet(ModelViewSet):
    queryset = ReadingQuestion.objects.all()
    serializer_class = ReadingQuestionSerializer
    filterset_class = ReadingQuestionTeacherFilter
    permission_classes = [IsTeacherOwnsQuestion]
    ordering_fields = ['from_number']
    ordering = ['from_number']
