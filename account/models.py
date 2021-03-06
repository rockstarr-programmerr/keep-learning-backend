from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_image_file_extension
from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image

from account.managers import (CustomUserManager, StudentManager,
                              TeacherManager, UserTypes)


class User(AbstractUser):
    Types = UserTypes

    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': _('A user with that email already exists.'),
        },
    )
    name = models.CharField(
        max_length=150,
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
    )
    user_type = models.CharField(
        max_length=20,
        choices=Types.choices,
    )
    avatar = models.ImageField(
        upload_to='users/avatar/%Y/%m',
        blank=True,
        validators=[validate_image_file_extension],
    )
    avatar_thumbnail = models.ImageField(
        upload_to='users/avatar_thumbnail/%Y/%m',
        blank=True,
        validators=[validate_image_file_extension],
    )
    username = models.CharField(
        max_length=150,
        blank=True,
    )

    # NOTE: Order of managers is important, first manager is considered "default" by Django.
    objects = CustomUserManager()
    teachers = TeacherManager()
    students = StudentManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.name} ({self.email}) - {self.get_user_type_display()}'

    def is_teacher(self):
        return self.user_type == self.Types.TEACHER

    def is_student(self):
        return self.user_type == self.Types.STUDENT
