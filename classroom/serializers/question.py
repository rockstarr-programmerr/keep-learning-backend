from django.utils.translation import gettext as _
from rest_framework import serializers

from classroom.models import ReadingQuestion


class ReadingQuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ReadingQuestion
        fields = [
            'pk', 'url', 'exercise', 'passage',
            'from_number', 'to_number', 'question_type',
            'answers', 'correct_answer',
        ]
        extra_kwargs = {
            'url': {'view_name': 'reading-question-detail'},
            'exercise': {'view_name': 'reading-exercise-detail'},
            'passage': {'min_value': 1},
            'from_number': {'min_value': 1},
            'to_number': {'min_value': 1},
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        self._validate_from_to_number(attrs)
        self._validate_question_not_exist(attrs)
        return attrs

    def _validate_from_to_number(self, attrs):
        from_number = attrs['from_number']
        to_number = attrs['to_number']
        if to_number is not None and not to_number > from_number:
            raise serializers.ValidationError(
                _('"To" must be greater than "From".')
            )

    def _validate_question_not_exist(self, attrs):
        from_number = attrs['from_number']
        exercise = attrs['exercise']
        question_range = exercise.get_question_range()

        if self.instance:
            if self.instance.to_number is not None:
                instance_range = range(self.instance.from_number, self.instance.to_number + 1)
            else:
                instance_range = [self.instance.from_number]
            for number in instance_range:
                try:
                    index = question_range.index(number)
                    question_range.pop(index)
                except ValueError:
                    pass

        if from_number in question_range:
            raise serializers.ValidationError(
                _('This question number already exists.')
            )

    # TODO: validation regarding `question_type` and `correct_answer`
