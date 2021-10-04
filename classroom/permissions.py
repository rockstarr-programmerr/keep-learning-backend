from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated


class IsTeacher(IsAuthenticated):
    message = _('Only teacher has permission for this.')

    def has_permission(self, request, view):
        return (
            super().has_permission(request, view) and
            request.user.is_teacher()
        )


class IsClassroomTeacher(IsTeacher):
    message = _('Only teacher of this class room has permission for this.')

    def has_object_permission(self, request, view, classroom):
        return (
            super().has_object_permission(request, view, classroom) and
            request.user == classroom.teacher
        )


class IsTeacherOwnsExercise(IsTeacher):
    message = _('Only teacher who owns this exercise has permission for this.')

    def has_object_permission(self, request, view, exercise):
        return (
            super().has_object_permission(request, view, exercise) and
            request.user == exercise.creator
        )


class IsStudent(IsAuthenticated):
    message = _('Only student has permission for this.')

    def has_permission(self, request, view):
        return (
            super().has_permission(request, view) and
            request.user.is_student()
        )


class IsClassroomStudent(IsStudent):
    message = _('Only student of this class room has permission for this.')

    def has_object_permission(self, request, view, classroom):
        return (
            super().has_object_permission(request, view, classroom) and
            request.user in classroom.students.all()
        )
