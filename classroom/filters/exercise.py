from django_filters import rest_framework as filters

from classroom.models import ReadingExercise


class ReadingExerciseFilter(filters.FilterSet):
    class Meta:
        model = ReadingExercise
        fields = {
            'identifier': ['exact', 'icontains'],
            'content': ['icontains'],
            'classrooms': ['exact'],  # TODO: how does this work?
        }

    @property
    def qs(self):
        parent = super().qs
        teacher = self.request.user
        exercises_pks = teacher.reading_exercises_created.all().values_list('pk', flat=True)
        qs = parent.filter(pk__in=list(exercises_pks))\
                   .select_related('creator')
        return qs
