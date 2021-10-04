from django.db import models
from django.utils.translation import gettext_lazy as _


class Question(models.Model):
    class Types(models.TextChoices):
        MULTIPLE_CHOICE = 'multiple_choice', _('Multiple choice')
        TRUE_FALSE = 'true_false', _('True/False/Not given')
        YES_NO = 'yes_no', _('Yes/No/Not given')
        FILL_BLANK = 'fill_blank', _('Fill in the blank')

    from_number = models.PositiveSmallIntegerField()
    to_number = models.PositiveSmallIntegerField()
    question_type = models.CharField(max_length=30, choices=Types.choices)
    correct_answer = models.CharField(max_length=255)

    class Meta:
        abstract = True
