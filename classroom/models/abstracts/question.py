from django.db import models
from django.utils.translation import gettext_lazy as _


class Question(models.Model):
    class Types(models.TextChoices):
        MULTIPLE_CHOICE = 'multiple_choice', _('Multiple choice')
        TRUE_FALSE = 'true_false', _('True / False / Not given')
        YES_NO = 'yes_no', _('Yes / No / Not given')
        FILL_BLANK = 'fill_blank', _('Fill in the blank')

    from_number = models.PositiveSmallIntegerField()
    to_number = models.PositiveSmallIntegerField(null=True)
    question_type = models.CharField(max_length=30, choices=Types.choices)
    correct_answer = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.get_question_number_display()} | {self.question_type} | {self.correct_answer[:50]}'

    def get_question_number_display(self):
        display = str(self.from_number)
        if self.to_number is not None and self.to_number != self.from_number:
            display += f' - {self.to_number}'
        return display
