from django.db import models
from django.contrib.auth import get_user_model

from .reading_submission import ReadingSubmission

User = get_user_model()


class ReadingSubmissionAnswer(models.Model):
    submission = models.ForeignKey(ReadingSubmission, on_delete=models.SET_NULL, null=True, related_name='answers')
    question_number = models.PositiveSmallIntegerField()
    content = models.CharField(max_length=255)

    class Meta:
        ordering = ['submission', 'question_number']
