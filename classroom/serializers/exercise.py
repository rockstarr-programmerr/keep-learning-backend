from django.utils.translation import gettext as _
from rest_framework import serializers

from classroom.models import (ReadingExercise, ReadingSubmission,
                              ReadingSubmissionAnswer)
from classroom.utils.serializer import ValidateUniqueTogetherMixin


class ReadingExerciseSerializer(ValidateUniqueTogetherMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ReadingExercise
        fields = ['pk', 'url', 'identifier', 'content']
        extra_kwargs = {
            'url': {'view_name': 'reading-exercise-detail'},
        }

    def validate_identifier(self, identifier):
        user = self.context['request'].user
        exercises = ReadingExercise.objects.filter(creator=user, identifier=identifier)
        self.unique_together_validate(exercises, _('An exercise with this identifier already exists.'))
        return identifier

    def save(self, **kwargs):
        teacher = self.context['request'].user
        kwargs['creator'] = teacher
        return super().save(**kwargs)


class _SubmitAnswerListSerializer(serializers.ListSerializer):
    def save(self, exercise=None):
        student = self.context['request'].user
        submission = self._create_submission(student, exercise)
        self._create_submission_answers(submission)

    def _create_submission(self, student, exercise):
        return ReadingSubmission.objects.create(submitter=student, exercise=exercise)

    def _create_submission_answers(self, submission):
        answers_to_create = []
        for answer in self.validated_data:
            answers_to_create.append(
                ReadingSubmissionAnswer(
                    submission=submission,
                    question_number=answer['question_number'],
                    content=answer['content'],
                )
            )
        ReadingSubmissionAnswer.objects.bulk_create(answers_to_create)


class ReadingExerciseSubmitSerializer(serializers.Serializer):
    question_number = serializers.IntegerField(min_value=1)
    content = serializers.CharField()

    class Meta:
        list_serializer_class = _SubmitAnswerListSerializer
