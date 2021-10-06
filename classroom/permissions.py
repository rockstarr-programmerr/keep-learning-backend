from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated


class IsTeacherOrReadOnly(IsAuthenticated):
    message = _('Only teacher can edit this resource, student can only read.')

    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        is_teacher = request.user.is_teacher()
        return (
            is_authenticated and (
                request.method in SAFE_METHODS or is_teacher
            )
        )


class IsStudent(IsAuthenticated):
    message = _('Only student has permission for this.')

    def has_permission(self, request, view):
        return (
            super().has_permission(request, view) and
            request.user.is_student()
        )
