from django.urls import path, include

from students import views

urlpatterns = [
    path('signup/', views.StudentSignUpView.as_view(), name='signup'),
]