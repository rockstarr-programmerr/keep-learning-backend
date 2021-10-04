from django.db import models

from .abstracts.question import Question
from .reading_exercise import ReadingExercise


class ReadingQuestion(Question):
    exercise = models.ForeignKey(ReadingExercise, on_delete=models.CASCADE, related_name='questions')

    class Meta:
        ordering = ['exercise', 'from_number']
