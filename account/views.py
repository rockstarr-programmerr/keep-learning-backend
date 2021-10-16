from django.contrib.auth import get_user_model
from django.utils.decorators import classonlymethod, method_decorator
from django.utils.translation import gettext as _
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from account import business
from account.serializers import (ChangePasswordSerializer, MeSerializer,
                                 RegisterTeacherSerializer, UserSerializer)

User = get_user_model()


@method_decorator(
    sensitive_post_parameters(
        'password', 'new_password', 'current_password'
    ),
    name='dispatch'
)
class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  GenericViewSet):
    """
    Endpoints for authentication:

    `/account/users/login/`: Login with credential (email, password), response with `access` and `refresh` token.

    `/account/users/token-refresh/`: Refresh token, response with another `access` and `refresh` token.
    """
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_teacher():
            classrooms = user.classrooms_teaching.all()
        else:
            classrooms = user.classrooms_studying.all()

        classrooms = classrooms.select_related('teacher').prefetch_related('students')

        users_pk = []
        for classroom in classrooms:
            teacher = classroom.teacher
            students = classroom.students.all()
            users_pk.append(teacher.pk)
            users_pk.extend(student.pk for student in students)

        return User.objects.filter(pk__in=users_pk)

    @action(
        methods=['POST'], detail=False, url_path='register-teacher',
        serializer_class=RegisterTeacherSerializer,
        permission_classes=[AllowAny],
    )
    def register_teacher(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        teacher = business.register_teacher(serializer.validated_data)
        serializer = self.get_serializer(instance=teacher)
        return Response(serializer.data)

    @action(
        detail=False, methods=['POST'],
        url_path='change-password',
        serializer_class=ChangePasswordSerializer,
    )
    def change_password(self, request):
        """
        Change logged-in user's password, return 403 if `current_password` is not correct.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        current_password = serializer.validated_data['current_password']
        new_password = serializer.validated_data['new_password']

        user = self.request.user
        if not user.check_password(current_password):
            raise PermissionDenied(_('Wrong password.'))

        user.set_password(new_password)
        user.save()
        return Response()


class MeViewSet(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                GenericViewSet):
    """
    Get/update information of current logged-in user.

    - To update avatar: send image with Content-Type = multipart/form-data

    - To remove avatar: send request with {"avatar": null}

    Maximum avatar size: **10MB**.
    If exceed, will response with `HTTP 413 Payload Too Large`.
    """
    serializer_class = MeSerializer

    @classonlymethod
    def as_view(cls, actions=None, **initkwargs):
        return super().as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
        }, **initkwargs)

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def get_object(self):
        return get_object_or_404(self.get_queryset(), pk=self.request.user.pk)
