from django.urls import path

from universities import views
from universities.views import UniversityCreateView, UniversityDeleteView, UniversityDetailView, UniversityUpdateView

urlpatterns = [
  path('list', views.university_list, name='universities-list'),
  path('<int:pk>/', UniversityDetailView.as_view(), name='university-detail'),
  path('create/', UniversityCreateView.as_view(), name='university-create'),
  path('<int:pk>/update/', UniversityUpdateView.as_view(), name='university-update'),
  path('delete/<int:pk>/', UniversityDeleteView.as_view(), name='university-delete'),

]
