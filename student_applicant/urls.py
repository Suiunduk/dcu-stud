from django.urls import path, include

from student_applicant import views

urlpatterns = [
    path('signup/', views.StudentSignUpView.as_view(), name='signup-applicant'),

]