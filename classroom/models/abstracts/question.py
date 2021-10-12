import re

from django.db import models
from django.utils.translation import gettext_lazy as _


class Question(models.Model):
    class Types(models.TextChoices):
        MULTIPLE_CHOICE = 'multiple_choice', _('Multiple choice')
        TRUE_FALSE = 'true_false', _('True / False / Not given')
        YES_NO = 'yes_no', _('Yes / No / Not given')
        FILL_BLANK = 'fill_blank', _('Fill in the blank')

    _DELEMITER = ' | '
    _TRUE = 'TRUE'
    _FALSE = 'FALSE'
    _YES = 'YES'
    _NO = 'NO'
    _NOT_GIVEN = 'NOT_GIVEN'

    number = models.PositiveSmallIntegerField()
    question_type = models.CharField(max_length=30, choices=Types.choices)
    choices = models.CharField(max_length=255, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.set_default_choices()
        return super().save(*args, **kwargs)

    def set_default_choices(self):
        if self.is_true_false():
            self.choices = self._DELEMITER.join([
                self._TRUE, self._FALSE, self._NOT_GIVEN
            ])
        elif self.is_yes_no():
            self.choices = self._DELEMITER.join([
                self._YES, self._NO, self._NOT_GIVEN
            ])
        elif not self.is_multiple_choice():
            self.choices = ''

    def is_multiple_choice(self):
        return self.question_type == self.Types.MULTIPLE_CHOICE

    def is_true_false(self):
        return self.question_type == self.Types.TRUE_FALSE

    def is_yes_no(self):
        return self.question_type == self.Types.YES_NO

    def is_fill_blank(self):
        return self.question_type == self.Types.FILL_BLANK

    def get_answers_content(self):
        answers = []
        for answer in self.answers.all():
            answers.append(answer.content)
        return answers

    def get_choices_content(self):
        return self.choices.split(self._DELEMITER)

    @classmethod
    def generate_choices_from_list(cls, choices):
        return cls._DELEMITER.join(choices)

    def check_answer(self, answer):
        # NOTE: don't use .values_list('content', flat=True) here,
        # because it will not utilize .prefetch_related('answers'),
        # which lead to more DB queries
        possible_answers = self.answers.all()
        possible_answers = [answer.content for answer in possible_answers]

        if self.is_fill_blank():
            answer = f' {answer} '  # Add 2 spaces to both side to help with regex matching

            for correct_answer in possible_answers:
                regex = correct_answer
                if regex.startswith('('):
                    regex = r'(?:' + regex[1:]

                regex = regex.replace(' (', r'(?:\s?')\
                             .replace(')', r')?')
                regex = r'\s*' + regex + r'\s*'

                match = re.match(regex, answer)
                if match:
                    match_str = match.group(0)
                    if match_str == answer:
                        return True

            return False
        else:
            return answer in possible_answers
