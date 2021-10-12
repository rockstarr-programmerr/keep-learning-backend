from django.utils.translation import gettext as _
from rest_framework import serializers

from account.serializers import UserSerializer
from classroom.models import Classroom, ReadingExercise
from classroom.utils.serializer import ValidateUniqueTogetherMixin


class ClassroomSerializer(ValidateUniqueTogetherMixin, serializers.HyperlinkedModelSerializer):
    teacher = UserSerializer(read_only=True)
    students = UserSerializer(many=True, read_only=True)
    reading_exercises = serializers.PrimaryKeyRelatedField(
        queryset=ReadingExercise.objects.all(),
        many=True,
    )

    class Meta:
        model = Classroom
        fields = [
            'pk', 'url', 'name', 'description', 'create_datetime',
            'teacher', 'students', 'reading_exercises',
        ]
        read_only_fields = [
            'create_datetime', 'teacher',
            'students', 'reading_exercises'
        ]
        extra_kwargs = {
            'url': {'view_name': 'classroom-detail'},
            # 'reading_exercises': {'view_name': 'reading-exercise-detail'},
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
    name = serializers.CharField(max_length=150)
    phone_number = serializers.CharField(required=False, allow_blank=True, max_length=20)


class RemoveStudentSerializer(serializers.Serializer):
    email = serializers.EmailField()


class AddReadingExerciseSerializer(serializers.Serializer):
    pk = serializers.IntegerField()


class RemoveReadingExerciseSerializer(serializers.Serializer):
    pk = serializers.IntegerField()


class _PassageDetailSerializer(serializers.Serializer):
    question_number = serializers.IntegerField()
    submitted_answer = serializers.CharField()
    possible_answers = serializers.ListField(child=serializers.CharField())
    is_correct = serializers.BooleanField()


class StudentReadingReportSerializer(serializers.Serializer):
    student = serializers.IntegerField(write_only=True)
    exercise = serializers.CharField(read_only=True)
    passage_1_total = serializers.IntegerField(read_only=True)
    passage_2_total = serializers.IntegerField(read_only=True)
    passage_3_total = serializers.IntegerField(read_only=True)
    total = serializers.IntegerField(read_only=True)
    band_score = serializers.FloatField(read_only=True)
    submitted = serializers.BooleanField(read_only=True)
    passage_1_detail = _PassageDetailSerializer(read_only=True, many=True)
    passage_2_detail = _PassageDetailSerializer(read_only=True, many=True)
    passage_3_detail = _PassageDetailSerializer(read_only=True, many=True)
