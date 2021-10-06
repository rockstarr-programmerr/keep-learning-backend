from django_filters import rest_framework as filters

from classroom.models import ReadingSubmission


class ReadingSubmissionFilter(filters.FilterSet):
    class Meta:
        model = ReadingSubmission
        fields = {
            'exercise': ['exact'],
            'submitter': ['exact'],
            'submit_datetime': ['gte', 'lte'],
        }

    @property
    def qs(self):
        parent = super().qs
        user = self.request.user

        if user.is_teacher():
            classrooms = user.classrooms_teaching.all()
            qs = parent.filter(exercise__classrooms__in=classrooms)
        else:
            qs = parent.filter(submitter=user)
        qs = qs.select_related('exercise__creator')\
               .prefetch_related('answers')

        return qs
