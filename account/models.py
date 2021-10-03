from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_image_file_extension
from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image

from account.managers import CustomUserManager, UserTypes

AVATAR_WIDTH = 256
AVATAR_HEIGHT = 256
AVATAR_THUMBNAIL_WIDTH = 64
AVATAR_THUMBNAIL_HEIGHT = 64


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

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f'{self.name} ({self.email})'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._make_thumbnail(self.avatar, AVATAR_WIDTH, AVATAR_HEIGHT)
        self._make_thumbnail(self.avatar_thumbnail, AVATAR_THUMBNAIL_WIDTH, AVATAR_THUMBNAIL_HEIGHT)

    @staticmethod
    def _make_thumbnail(image, width, height):
        if image and (
            image.width > width or
            image.height > height
        ):
            with Image.open(image.path) as f:
                f.thumbnail((width, height))
                f.save(image.path)

    def is_teacher(self):
        return self.user_type == self.Types.TEACHER

    def is_student(self):
        return self.user_type == self.Types.STUDENT
