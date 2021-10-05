from rest_framework.viewsets import ModelViewSet

from classroom.filters import ReadingQuestionFilter
from classroom.models import ReadingQuestion
from classroom.permissions import IsTeacherOwnsQuestion
from classroom.serializers import ReadingQuestionSerializer


class ReadingQuestionViewSet(ModelViewSet):
    queryset = ReadingQuestion.objects.all()
    serializer_class = ReadingQuestionSerializer
    filterset_class = ReadingQuestionFilter
    permission_classes = [IsTeacherOwnsQuestion]
    ordering_fields = ['from_number']
    ordering = ['from_number']
