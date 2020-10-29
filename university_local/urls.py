from django.urls import path

from university_local import views
from university_local.views import UniversityCreateView, UniversityDeleteView, UniversityDetailView, UniversityUpdateView, downloadcsv

urlpatterns = [
  path('list', views.university_list, name='universities-list'),
  path('<int:pk>/', UniversityDetailView.as_view(), name='university-detail'),
  path('create/', UniversityCreateView.as_view(), name='university-create'),
  path('<int:pk>/update/', UniversityUpdateView.as_view(), name='university-update'),
  path('delete/<int:pk>/', UniversityDeleteView.as_view(), name='university-delete'),
  path('upload/', views.simple_upload, name='university-upload'),
  path('downloadcsv/', downloadcsv, name='download-csv'),
]
