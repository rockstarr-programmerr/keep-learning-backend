from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Classroom(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': User.Types.TEACHER},
        related_name='classrooms_teaching',
    )
    students = models.ManyToManyField(
        User,
        limit_choices_to={'user_type': User.Types.STUDENT},
        related_name='classrooms_studying',
    )
    create_datetime = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-create_datetime']
