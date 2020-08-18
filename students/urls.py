from django.urls import path, include

from students import views
from students.views import StudentDetailView, StudentCreateView, StudentUpdateView, StudentDeleteView, \
    StudentProfileView

urlpatterns = [
    path('signup/', views.StudentSignUpView.as_view(), name='signup'),
    path('list', views.student_list, name='student-list'),
    path('<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('profile/<int:pk>/', StudentProfileView.as_view(), name='student-profile'),
    path('create/', StudentCreateView.as_view(), name='student-create'),
    path('<int:pk>/update/', StudentUpdateView.as_view(), name='student-update'),
    path('delete/<int:pk>/', StudentDeleteView.as_view(), name='student-delete'),

]
