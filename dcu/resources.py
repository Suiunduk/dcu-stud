from import_export import resources

from student_abroad.models import StudentAbroadCommon


class StudentResource(resources.ModelResource):
    class Meta:
        model = StudentAbroadCommon
