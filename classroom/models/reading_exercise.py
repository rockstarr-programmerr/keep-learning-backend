from django.contrib.auth import get_user_model
from django.db import models

from .classroom import Classroom

User = get_user_model()


class ReadingExercise(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reading_exercises_created')
    identifier = models.CharField(max_length=20)
    content = models.TextField()
    classrooms = models.ManyToManyField(Classroom, related_name='reading_exercises')

    class Meta:
        ordering = ['identifier']
        unique_together = ['creator', 'identifier']

    def __str__(self):
        display = self.identifier
        if self.creator:
            display += f' | {self.creator.email}'
        return display

    def get_question_range(self):
        question_numbers = self.questions.order_by('from_number').values('from_number', 'to_number')
        question_range = []
        for number in question_numbers:
            from_number = number['from_number']
            to_number = number['to_number']
            if to_number is None:
                question_range.append(from_number)
            else:
                question_range.extend(range(from_number, to_number + 1))
        return question_range
