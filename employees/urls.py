from django.urls import path, include

from employees import views

urlpatterns = [
    path('signup/', views.EmployeeSignUpView.as_view(), name='signup'),
]
