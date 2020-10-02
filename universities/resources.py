from import_export import resources

from universities.models import University


class UniversityResource(resources.ModelResource):
    class Meta:
        model = University
