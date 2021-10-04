from django.utils.translation import gettext as _
from rest_framework import serializers

from account.serializers import UserSerializer
from classroom.models import Classroom
from classroom.utils.serializer import ValidateUniqueTogetherMixin


class ClassroomTeacherSerializer(ValidateUniqueTogetherMixin, serializers.HyperlinkedModelSerializer):
    teacher = UserSerializer(read_only=True)
    students = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Classroom
        fields = [
            'pk', 'url', 'name', 'description', 'create_datetime',
            'teacher', 'students', 'reading_exercises',
        ]
        extra_kwargs = {
            'url': {'view_name': 'classroom-teacher-detail'},
            'reading_exercises': {'view_name': 'reading-exercise-teacher-detail'},
            'create_datetime': {'read_only': True},
        }

    def validate_name(self, name):
        teacher = self.context['request'].user
        classrooms = Classroom.objects.filter(teacher=teacher, name=name)
        self.unique_together_validate(classrooms, _('This classroom already exists.'))
        return name

    def save(self, **kwargs):
        teacher = self.context['request'].user
        kwargs['teacher'] = teacher
        return super().save(**kwargs)


class AddStudentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField(required=False, max_length=150)
    phone_number = serializers.CharField(required=False, max_length=20)


class RemoveStudentSerializer(serializers.Serializer):
    email = serializers.EmailField()


class AddReadingExerciseSerializer(serializers.Serializer):
    pk = serializers.IntegerField()


class RemoveReadingExerciseSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
