from django.db import models

from .abstracts.question import Question
from .reading_exercise import ReadingExercise
from .reading_answer import ReadingAnswer


class ReadingQuestion(Question):
    exercise = models.ForeignKey(ReadingExercise, on_delete=models.CASCADE, related_name='questions')
    passage = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ['exercise']

    def __str__(self):
        return f'{self.exercise.identifier} | {self.get_question_type_display()}'

    def create_answers(self, answers):
        contents = answers.split(self._DELEMITER)
        answers_objs = [
            ReadingAnswer(question=self, content=content)
            for content in contents
        ]
        ReadingAnswer.objects.bulk_create(answers_objs)

    def replace_answers(self, answers):
        self.answers.all().delete()
        self.create_answers(answers)
