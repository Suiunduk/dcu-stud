from import_export import resources

from students.models import Student


class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
