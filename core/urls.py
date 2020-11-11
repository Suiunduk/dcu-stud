from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', homepage, name='homepage'),
    path('announcement/<int:pk>/', AnnouncementDetailView.as_view(), name='announcement'),
    path('parent_type/list', views.parent_types_list, name='parent-types-list'),
    path('parent_type/create/', ParentTypeCreateView.as_view(), name='parent-type-create'),
    path('parent_type/update/<int:pk>', ParentTypeUpdateView.as_view(), name='parent-type-update'),
    path('parent_type/delete/<int:pk>', ParentTypeDeleteView.as_view(), name='parent-type-delete'),
    path('gender/list', views.genders_list, name='genders-list'),
    path('gender/create/', GenderCreateView.as_view(), name='gender-create'),
    path('gender/update/<int:pk>', GenderUpdateView.as_view(), name='gender-update'),
    path('gender/delete/<int:pk>', GenderDeleteView.as_view(), name='gender-delete'),
    path('type_of_applying/list', views.types_of_applying_list, name='types-of-applying-list'),
    path('type_of_applying/create/', TypeOfApplyingCreateView.as_view(), name='type-of-applying-create'),
    path('type_of_applying/update/<int:pk>', TypeOfApplyingUpdateView.as_view(), name='type-of-applying-update'),
    path('type_of_applying/delete/<int:pk>', TypeOfApplyingDeleteView.as_view(), name='type-of-applying-delete'),
    path('education_program/list', views.education_programs_list, name='education-programs-list'),
    path('education_program/create/', EducationProgramCreateView.as_view(), name='education-program-create'),
    path('education_program/update/<int:pk>', EducationProgramUpdateView.as_view(), name='education-program-update'),
    path('education_program/delete/<int:pk>', EducationProgramDeleteView.as_view(), name='education-program-delete'),
    path('education_form/list', views.education_forms_list, name='education-forms-list'),
    path('education_form/create/', EducationFormCreateView.as_view(), name='education-form-create'),
    path('education_form/update/<int:pk>', EducationFormUpdateView.as_view(), name='education-form-update'),
    path('education_form/delete/<int:pk>', EducationFormDeleteView.as_view(), name='education-form-delete'),
    path('status/list', views.statuses_list, name='statuses-list'),
    path('status/create/', StatusCreateView.as_view(), name='status-create'),
    path('status/update/<int:pk>', StatusUpdateView.as_view(), name='status-update'),
    path('status/delete/<int:pk>', StatusDeleteView.as_view(), name='status-delete'),
    path('country/list', views.countries_list, name='countries-list'),
    path('country/create/', CountryCreateView.as_view(), name='country-create'),
    path('country/update/<int:pk>', CountryUpdateView.as_view(), name='country-update'),
    path('country/delete/<int:pk>', CountryDeleteView.as_view(), name='country-delete'),
]
