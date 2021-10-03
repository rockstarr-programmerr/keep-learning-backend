from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from classroom.filters import ClassroomTeacherFilter
from classroom.models import Classroom
from classroom.permissions import IsClassroomTeacher
from classroom.serializers import ClassroomTeacherSerializer


class ClassroomTeacherViewSet(ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomTeacherSerializer
    filterset_class = ClassroomTeacherFilter
    permission_classes = [IsClassroomTeacher]
    ordering_fields = ['create_datetime', 'name']
    ordering = ['-create_datetime']
