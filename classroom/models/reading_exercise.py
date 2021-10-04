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
