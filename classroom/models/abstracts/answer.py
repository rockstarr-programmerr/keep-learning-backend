from django.db import models


class Answer(models.Model):
    letter = models.CharField(max_length=1, blank=True)
    content = models.TextField()

    class Meta:
        abstract = True
