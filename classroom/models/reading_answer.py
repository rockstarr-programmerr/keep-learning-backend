from django.db import models

from .abstracts.answer import Answer


class ReadingAnswer(Answer):
    question = models.ForeignKey('ReadingQuestion', on_delete=models.CASCADE, related_name='answers')

    class Meta:
        ordering = ['content']
