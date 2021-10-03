from django_filters import rest_framework as filters

from classroom.models import Classroom


class ClassroomTeacherFilter(filters.FilterSet):
    class Meta:
        model = Classroom
        fields = {
            'name': ['exact', 'icontains'],
            'description': ['icontains'],
            'create_datetime': ['gte', 'lte'],
        }

    @property
    def qs(self):
        parent = super().qs
        teacher = self.request.user
        classrooms_pks = teacher.classrooms_teaching.all().values_list('pk', flat=True)
        qs = parent.filter(pk__in=list(classrooms_pks))\
                   .select_related('teacher')\
                   .prefetch_related('students')
        return qs
