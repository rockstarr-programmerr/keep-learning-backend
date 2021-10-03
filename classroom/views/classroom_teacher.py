from django.utils.translation import gettext as _
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from classroom import business
from classroom.filters import ClassroomTeacherFilter
from classroom.models import Classroom
from classroom.permissions import IsClassroomTeacher
from classroom.serializers import (AddStudentSerializer,
                                   ClassroomTeacherSerializer,
                                   RemoveStudentSerializer)


class ClassroomTeacherViewSet(ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomTeacherSerializer
    filterset_class = ClassroomTeacherFilter
    permission_classes = [IsClassroomTeacher]
    ordering_fields = ['create_datetime', 'name']
    ordering = ['-create_datetime']

    @action(
        methods=['POST'], detail=True, url_path='add-students',
        serializer_class=AddStudentSerializer,
    )
    def add_students(self, request, pk):
        """Add students to this classroom.

        If an email doesn't exist in DB yet, a new student account will be created.

        If an email exists, the existing student will be added to this classroom.

        In case of creating new student account, a temporary password will be sent to that student.
        Teacher cannot see this password.
        """
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        classroom = self.get_object()
        business.add_students_to_classroom(classroom, serializer.validated_data)
        return Response({
            'message': _(
                "Your students will receive an email with a temporary password. "
                "Tell them to login with it."
            )
        })

    @action(
        methods=['POST'], detail=True, url_path='remove-students',
        serializer_class=RemoveStudentSerializer,
    )
    def remove_students(self, request, pk):
        """Remove students from this classroom.

        The student account will **NOT** be deleted, it will just be removed from this classroom.
        """
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        emails = [data['email'] for data in serializer.validated_data]
        classroom = self.get_object()
        business.remove_students_from_classroom(classroom, emails)
        return Response()
