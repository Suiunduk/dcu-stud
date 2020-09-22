from django.urls import path, include

from students_in_kg import views
from students_in_kg.views import StudentDetailView, StudentCreateView, StudentCreateViewForEmp, StudentUpdateView, \
    StudentDeleteView

urlpatterns = [
    path('list', views.student_list, name='student-abroad-list'),
    path('<int:pk>/', StudentDetailView.as_view(), name='student-abroad-detail'),
    path('create/', StudentCreateView.as_view(), name='student-abroad-create'),
    path('create/<int:fk>', StudentCreateViewForEmp.as_view(), name='student-abroad-create-emp'),
    path('<int:pk>/update/', StudentUpdateView.as_view(), name='student-abroad-update'),
    path('delete/<int:pk>/', StudentDeleteView.as_view(), name='student-abroad-delete'),
]
