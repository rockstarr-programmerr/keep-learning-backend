from rest_framework import serializers

from account.serializers import UserSerializer
from classroom.models import ReadingSubmission


class ReadingSubmissionSerializer(serializers.HyperlinkedModelSerializer):
    submitter = UserSerializer()
    answers = serializers.ListField(source='get_answers')

    class Meta:
        model = ReadingSubmission
        fields = [
            'pk', 'url', 'exercise',
            'submitter', 'submit_datetime', 'answers',
        ]
        extra_kwargs = {
            'url': {'view_name': 'reading-submission-detail'},
            'exercise': {'view_name': 'reading-exercise-detail'},
        }
