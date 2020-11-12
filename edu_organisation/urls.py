from django.urls import path

from edu_organisation import views
from edu_organisation.views import OrganisationCreateView, OrganisationDeleteView, OrganisationDetailView, \
    OrganisationUpdateView

urlpatterns = [
  path('list', views.organisation_list, name='organisations-list'),
  path('<int:pk>/', OrganisationDetailView.as_view(), name='organisation-detail'),
  path('create/', OrganisationCreateView.as_view(), name='organisation-create'),
  path('<int:pk>/update/', OrganisationUpdateView.as_view(), name='organisation-update'),
  path('delete/<int:pk>/', OrganisationDeleteView.as_view(), name='organisation-delete'),
  path('upload', views.edu_org_upload, name='organisation-upload')
]
