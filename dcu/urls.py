"""dcu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView

from dcu import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('favicon.ico/', RedirectView.as_view(url='/static/img/favicon.ico', permanent=True)),
    path('student_abroad/', include('student_abroad.urls')),
    path('student_applicant/', include('student_applicant.urls')),
    path('student_foreign/', include('student_foreign.urls')),
    path('university_local/', include('university_local.urls')),
    path('edu_organisation/', include('edu_organisation.urls')),
    path('university_employee/', include('university_employee.urls')),
    path('accounts/', include('users.urls')),
    path('announcements/', include('announcement.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
