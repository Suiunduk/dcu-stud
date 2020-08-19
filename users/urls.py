from django.urls import path, include

from django.views.generic.base import TemplateView

from users import views

urlpatterns = [
    #path('signup/', views.SignUp.as_view(), name='signup'),
    #path('profile/', TemplateView.as_view(template_name='profile.html'), name='profile'),
    path('change-password/', views.change_password, name='change_password')
]
