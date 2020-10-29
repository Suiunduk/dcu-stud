from django.urls import path, include

from student_foreign import views
from student_foreign.views import StudentDetailView, StudentCreateView, StudentCreateViewForEmp, StudentUpdateView, \
    StudentDeleteView

urlpatterns = [
    path('list', views.student_list, name='student-foreign-list'),
    path('<int:pk>/', StudentDetailView.as_view(), name='student-foreign-detail'),
    path('create/', StudentCreateView.as_view(), name='student-foreign-create'),
    path('create/<int:fk>', StudentCreateViewForEmp.as_view(), name='student-foreign-create-emp'),
    path('<int:pk>/update/', StudentUpdateView.as_view(), name='student-foreign-update'),
    path('delete/<int:pk>/', StudentDeleteView.as_view(), name='student-foreign-delete'),
    path('upload/', views.student_upload, name='student-foreign-upload'),
]
