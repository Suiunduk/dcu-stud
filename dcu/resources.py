from import_export import resources

from student_abroad.models import StudentAbroad


class StudentResource(resources.ModelResource):
    class Meta:
        model = StudentAbroad
