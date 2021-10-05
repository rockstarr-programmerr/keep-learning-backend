from django.utils.translation import gettext as _
from rest_framework import serializers

from classroom.models import ReadingQuestion


class ReadingQuestionSerializer(serializers.HyperlinkedModelSerializer):
    answers = serializers.CharField(source='get_answers_content')

    class Meta:
        model = ReadingQuestion
        fields = [
            'pk', 'url', 'exercise', 'passage',
            'number', 'question_type',
            'choices', 'answers',
        ]
        extra_kwargs = {
            'url': {'view_name': 'reading-question-detail'},
            'exercise': {'view_name': 'reading-exercise-detail'},
            'passage': {'min_value': 1},
            'number': {'min_value': 1},
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        self._validate_question_not_exist(attrs)
        self._handle_get_answers_content(attrs)
        return attrs

    def _validate_question_not_exist(self, attrs):
        number = attrs.get('number')
        if number is None:
            return

        exercise = attrs.get('exercise') or self.instance.exercise  # If `attrs` don't have 'exercise',
                                                                    # there should be `self.instance`
        question_range = exercise.get_question_range()

        if self.instance:
            try:
                index = question_range.index(self.instance.number)
                question_range.pop(index)
            except ValueError:
                pass

        if number in question_range:
            raise serializers.ValidationError(
                _('This question number already exists.')
            )

    def _handle_get_answers_content(self, attrs):
        if 'get_answers_content' in attrs:
            attrs['answers'] = attrs.pop('get_answers_content')

    def create(self, validated_data):
        has_answers = 'answers' in validated_data
        if has_answers:
            answers = validated_data.pop('answers')

        question = super().create(validated_data)

        if has_answers:
            question.create_answers(answers)

        return question

    def update(self, question, validated_data):
        if 'answers' in validated_data:
            answers = validated_data.pop('answers')
            question.replace_answers(answers)

        return super().update(question, validated_data)
