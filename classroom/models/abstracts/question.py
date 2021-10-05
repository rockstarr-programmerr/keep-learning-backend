from django.db import models
from django.utils.translation import gettext_lazy as _


class Question(models.Model):
    class Types(models.TextChoices):
        MULTIPLE_CHOICE = 'multiple_choice', _('Multiple choice')
        TRUE_FALSE = 'true_false', _('True / False / Not given')
        YES_NO = 'yes_no', _('Yes / No / Not given')
        FILL_BLANK = 'fill_blank', _('Fill in the blank')

    ANSWERS_DELEMITER = ' | '
    _TRUE = 'TRUE'
    _FALSE = 'FALSE'
    _YES = 'YES'
    _NO = 'NO'
    _NOT_GIVEN = 'NOT_GIVEN'

    from_number = models.PositiveSmallIntegerField()
    to_number = models.PositiveSmallIntegerField(null=True)
    question_type = models.CharField(max_length=30, choices=Types.choices)
    answers = models.CharField(max_length=255, blank=True)
    correct_answer = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.get_question_number_display()} | {self.question_type} | {self.correct_answer[:50]}'

    def save(self, *args, **kwargs):
        self.set_default_answers()
        return super().save(*args, **kwargs)

    def get_question_number_display(self):
        display = str(self.from_number)
        if self.to_number is not None and self.to_number != self.from_number:
            display += f' - {self.to_number}'
        return display

    def set_default_answers(self):
        if self.is_true_false():
            self.answers = self.ANSWERS_DELEMITER.join([
                self._TRUE, self._FALSE, self._NOT_GIVEN
            ])
        elif self.is_yes_no():
            self.answers = self.ANSWERS_DELEMITER.join([
                self._YES, self._NO, self._NOT_GIVEN
            ])
        elif not self.is_multiple_choice():
            self.answers = ''

    def is_true_false(self):
        return self.question_type == self.Types.TRUE_FALSE

    def is_yes_no(self):
        return self.question_type == self.Types.YES_NO

    def is_multiple_choice(self):
        return self.question_type == self.Types.MULTIPLE_CHOICE
