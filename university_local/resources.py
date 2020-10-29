from import_export import resources

from university_local.models import University


class UniversityResource(resources.ModelResource):
    class Meta:
        model = University
