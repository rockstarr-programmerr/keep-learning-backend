from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from classroom.business.teacher import classroom as teacher_business
from classroom.business.all.student_report import ReadingReportMaker
from classroom.filters import ClassroomFilter
from classroom.models import Classroom
from classroom.permissions import IsTeacherOrReadOnly
from classroom.serializers import (AddReadingExerciseSerializer,
                                   AddStudentSerializer, ClassroomSerializer,
                                   RemoveReadingExerciseSerializer,
                                   RemoveStudentSerializer,
                                   StudentReadingReportSerializer)

User = get_user_model()


class ClassroomViewSet(ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    filterset_class = ClassroomFilter
    permission_classes = [IsTeacherOrReadOnly]
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
        teacher_business.add_students_to_classroom(classroom, serializer.validated_data)
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
        teacher_business.remove_students_from_classroom(classroom, emails)
        return Response()

    @action(
        methods=['POST'], detail=True, url_path='add-reading-exercises',
        serializer_class=AddReadingExerciseSerializer,
    )
    def add_reading_exercises(self, request, pk):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        exercise_pks = [data['pk'] for data in serializer.validated_data]
        classroom = self.get_object()
        teacher_business.add_reading_exercises_to_classroom(classroom, exercise_pks, request.user)
        return Response()

    @action(
        methods=['POST'], detail=True, url_path='remove-reading-exercises',
        serializer_class=RemoveReadingExerciseSerializer,
    )
    def remove_reading_exercises(self, request, pk):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        exercise_pks = [data['pk'] for data in serializer.validated_data]
        classroom = self.get_object()
        teacher_business.remove_reading_exercises_to_classroom(classroom, exercise_pks)
        return Response()

    @action(
        methods=['GET'], detail=True, url_path='student-reading-report',
        serializer_class=StudentReadingReportSerializer,
    )
    def student_reading_report(self, request, pk):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        classroom = self.get_object()
        student = get_object_or_404(User.students.all(), pk=serializer.validated_data['student'])
        report_maker = ReadingReportMaker(classroom, student)
        report = report_maker.make()
        return Response(report)
