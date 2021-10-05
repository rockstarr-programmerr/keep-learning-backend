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
        user = self.request.user

        if user.is_teacher():
            qs = parent.filter(creator=user)
        else:
            qs = parent.filter(classrooms__in=user.classrooms_studying.all())  # TODO: test
        qs = qs.select_related('creator')

        return qs
