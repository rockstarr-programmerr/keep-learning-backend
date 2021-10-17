from django.db import models


class Answer(models.Model):
    content = models.CharField(max_length=255)

    class Meta:
        abstract = True
