from django.urls import path, include

from student_abroad import views
from student_abroad.views import StudentDetailView, StudentCreateView, StudentUpdateView, StudentDeleteView, \
     StudentCreateViewForEmp, DocumentUploadView, DocumentDetailView, DocumentUpdateView

urlpatterns = [
    path('signup/', views.StudentSignUpView.as_view(), name='signup'),
    path('signup_wizard/', views.StudentSignUpWizardView.as_view(), name='signup-wizard'),
    path('list', views.student_list, name='student-list'),
    path('<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('create/', StudentCreateView.as_view(), name='student-create'),
    path('create/<int:fk>', StudentCreateViewForEmp.as_view(), name='student-create-emp'),
    path('<int:pk>/update/', StudentUpdateView.as_view(), name='student-update'),
    path('delete/<int:pk>/', StudentDeleteView.as_view(), name='student-delete'),
    path('message/', views.contact_view, name='email-send'),
    path('success/', views.email_success, name='email-success'),
    path('export/', views.export_data, name='export-student_abroad'),
    path('upload/<int:pk>', DocumentUploadView.as_view(), name='document-upload'),
    path('document/<int:pk>/', DocumentDetailView.as_view(), name='document-detail'),
    path('document/update/<int:pk>/', DocumentUpdateView.as_view(), name='document-update'),
    path('document/delete/<int:pk>/', views.document_delete, name='document-delete')
]
