from django.contrib.auth.models import UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


def get_first_part_of_email(email):
    return email.split('@')[0]


class UserTypes(models.TextChoices):
    TEACHER = 'teacher', _('teacher')
    STUDENT = 'student', _('student')
    ADMIN = 'admin', _('admin')


class CustomUserManager(UserManager):
    """
    Customize to allow creating user with just email, no need username
    """
    def create_user(self, username=None, email=None, password=None, **extra_fields):
        assert bool(email), 'Email is required for creating user.'
        username = get_first_part_of_email(email)
        return super().create_user(username, email=email, password=password, **extra_fields)

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        assert bool(email), 'Email is required for creating user.'
        username = get_first_part_of_email(email)
        if not 'user_type' in extra_fields:
            user_type = UserTypes.ADMIN
            extra_fields['user_type'] = user_type
        return super().create_superuser(username, email=email, password=password, **extra_fields)

    def create_teacher(self, email=None, password=None, **extra_fields):
        extra_fields['user_type'] = UserTypes.TEACHER
        return self.create_user(email=email, password=password, **extra_fields)
