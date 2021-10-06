from copy import copy

from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.reverse import reverse

from account.serializers import UserSerializer
from classroom.models import Classroom
from classroom.utils.serializer import ValidateUniqueTogetherMixin


class _StudentSerializer(UserSerializer):
    reading_report_url = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = copy(UserSerializer.Meta.fields)
        fields.append('reading_report_url')

    def get_reading_report_url(self, student):
        request = self.context['request']
        classroom_pk = self.context['view'].kwargs['pk']
        url = reverse('classroom-student-reading-report', kwargs={'pk': classroom_pk}, request=request)
        url += f'?student={student.pk}'
        return url


class ClassroomSerializer(ValidateUniqueTogetherMixin, serializers.HyperlinkedModelSerializer):
    teacher = UserSerializer(read_only=True)
    students = _StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Classroom
        fields = [
            'pk', 'url', 'name', 'description', 'create_datetime',
            'teacher', 'students', 'reading_exercises',
        ]
        extra_kwargs = {
            'url': {'view_name': 'classroom-detail'},
            'reading_exercises': {'view_name': 'reading-exercise-detail'},
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


class StudentReadingReportSerializer(serializers.Serializer):
    student = serializers.IntegerField(write_only=True)
