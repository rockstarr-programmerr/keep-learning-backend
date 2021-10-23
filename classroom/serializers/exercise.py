from django.conf import settings
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


class _ReadingExerciseAnswerSerializer(serializers.Serializer):
    question_number = serializers.IntegerField(min_value=1)
    content = serializers.CharField()


class ReadingExerciseSubmitSerializer(serializers.Serializer):
    time_taken = serializers.DurationField(
        help_text='Number of seconds, or a string in this format: "[DD] [HH:[MM:]]ss[.uuuuuu]".'
    )
    answers = _ReadingExerciseAnswerSerializer(many=True)

    def save(self, exercise=None):
        student = self.context['request'].user
        if exercise.submissions.filter(submitter=student).exists():
            raise serializers.ValidationError(
                _('You already submitted answers for this exercise.')
            )
        submission = self._create_submission(student, exercise)
        self._create_submission_answers(submission)

    def _create_submission(self, student, exercise):
        time_taken = self.validated_data['time_taken']
        return ReadingSubmission.objects.create(
            submitter=student,
            exercise=exercise,
            time_taken=time_taken,
        )

    def _create_submission_answers(self, submission):
        answers_to_create = []
        for answer in self.validated_data['answers']:
            answers_to_create.append(
                ReadingSubmissionAnswer(
                    submission=submission,
                    question_number=answer['question_number'],
                    content=answer['content'],
                )
            )
        ReadingSubmissionAnswer.objects.bulk_create(answers_to_create)


class ReadingExerciseUploadImgSerializer(serializers.Serializer):
    image = serializers.ImageField(write_only=True)
    image_url = serializers.URLField(read_only=True)

    def validate_image(self, image):
        if not image:
            return image

        size = image.size / 1e6  # bytes to megabytes
        if size > settings.MAX_UPLOAD_SIZE_MEGABYTES:
            raise serializers.ValidationError(
                _('File size must not exceed %dMB.') % settings.MAX_UPLOAD_SIZE_MEGABYTES,
                code='exceed_max_upload_size'
            )

        return image
