from django.db import models


class ReadingExercise(models.Model):
    identifier = models.CharField(max_length=20)
    content = models.TextField()

    class Meta:
        ordering = ['identifier']
