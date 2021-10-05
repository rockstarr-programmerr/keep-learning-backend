from django_filters import rest_framework as filters

from classroom.models import ReadingQuestion


class ReadingQuestionFilter(filters.FilterSet):
    class Meta:
        model = ReadingQuestion
        fields = {
            'exercise': ['exact'],
            'passage': ['exact'],
            'number': ['exact', 'gte', 'lte'],
        }

    @property
    def qs(self):
        parent = super().qs
        user = self.request.user

        if user.is_teacher():
            qs = parent.filter(exercise__creator=user)
        else:
            qs = parent.filter(exercise__classrooms__in=user.classrooms_studying.all())
        qs = qs.select_related('exercise__creator')

        return qs
