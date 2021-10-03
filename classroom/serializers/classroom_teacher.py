from django.utils.translation import gettext as _
from rest_framework import serializers

from account.serializers import UserSerializer
from classroom.models import Classroom


class ClassroomTeacherSerializer(serializers.HyperlinkedModelSerializer):
    teacher = UserSerializer(read_only=True)
    students = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Classroom
        fields = [
            'pk', 'url', 'name', 'description', 'create_datetime',
            'teacher', 'students',
        ]
        extra_kwargs = {
            'url': {'view_name': 'classroom-teacher-detail'},
            'create_datetime': {'read_only': True},
        }

    def validate_name(self, name):
        request = self.context['request']
        teacher = request.user
        classrooms = Classroom.objects.filter(teacher=teacher, name=name)
        error = False

        if request.method in ('PUT', 'PATCH'):
            pk = request.parser_context['kwargs']['pk']
            classroom = classrooms.first()
            if classroom:
                error = classroom.pk != pk
        else:
            error = classrooms.exists()

        if error:
            raise serializers.ValidationError(
                detail=_('This classroom already exists.'),
                code='unique_together'
            )

        return name

    def save(self, **kwargs):
        teacher = self.context['request'].user
        kwargs['teacher'] = teacher
        return super().save(**kwargs)
