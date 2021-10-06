from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from .reading_exercise import ReadingExercise

User = get_user_model()


class ReadingSubmission(models.Model):
    exercise = models.ForeignKey(ReadingExercise, on_delete=models.CASCADE, related_name='submissions')
    submitter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reading_submissions')
    submit_datetime = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['exercise', 'submitter']
