from rest_framework.viewsets import ReadOnlyModelViewSet

from classroom.filters import ReadingSubmissionFilter
from classroom.models import ReadingSubmission
from classroom.serializers import ReadingSubmissionSerializer


class ReadingSubmissionViewSet(ReadOnlyModelViewSet):
    queryset = ReadingSubmission.objects.all()
    serializer_class = ReadingSubmissionSerializer
    filterset_class = ReadingSubmissionFilter
    ordering_fields = ['exercise', 'submitter', 'submit_datetime']
    ordering = ['exercise', 'submitter', 'submit_datetime']
