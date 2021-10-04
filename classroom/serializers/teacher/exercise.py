from django.utils.translation import gettext as _
from rest_framework import serializers

from classroom.models import ReadingExercise
from classroom.utils.serializer import ValidateUniqueTogetherMixin


class ReadingExerciseSerializer(ValidateUniqueTogetherMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ReadingExercise
        fields = ['pk', 'url', 'identifier', 'content']
        extra_kwargs = {
            'url': {'view_name': 'reading-exercise-teacher-detail'},
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
