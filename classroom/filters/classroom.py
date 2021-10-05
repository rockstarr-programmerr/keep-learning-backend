from django_filters import rest_framework as filters

from classroom.models import Classroom


class ClassroomFilter(filters.FilterSet):
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

        if self.request.user.is_teacher():
            classrooms = self.teacher_classrooms
        else:
            classrooms = self.student_classrooms
        classrooms_pks = list(classrooms.values_list('pk', flat=True))

        qs = parent.filter(pk__in=classrooms_pks)\
                   .select_related('teacher')\
                   .prefetch_related('students')
        return qs

    @property
    def teacher_classrooms(self):
        teacher = self.request.user
        return teacher.classrooms_teaching.all()

    @property
    def student_classrooms(self):
        student = self.request.user
        return student.classrooms_studying.all()
