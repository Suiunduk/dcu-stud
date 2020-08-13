from django.urls import path, include

from django.views.generic.base import TemplateView

urlpatterns = [
    #path('signup/', views.SignUp.as_view(), name='signup'),
    path('profile/', TemplateView.as_view(template_name='profile.html'), name='profile'),
]
