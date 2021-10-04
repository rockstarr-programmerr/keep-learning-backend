from django.db import models

from .abstracts.answer import Answer
from .reading_question import ReadingQuestion


class ReadingAnswer(Answer):
    question = models.ForeignKey(ReadingQuestion, on_delete=models.CASCADE, related_name='answers')

    class Meta:
        ordering = ['question', 'letter', 'pk']

    def __str__(self):
        return f'{self.letter}. {self.content[:50]}'
