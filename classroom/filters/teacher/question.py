from django_filters import rest_framework as filters

from classroom.models import ReadingQuestion


class ReadingQuestionTeacherFilter(filters.FilterSet):
    class Meta:
        model = ReadingQuestion
        fields = {
            'exercise': ['exact'],
        }

    @property
    def qs(self):
        parent = super().qs
        user = self.request.user
        exercises = user.reading_exercises_created.all()
        questions_pks = ReadingQuestion.objects.filter(exercise__in=exercises).values_list('pk', flat=True)
        qs = parent.filter(pk__in=list(questions_pks))\
                   .select_related('exercise__creator')
        return qs
