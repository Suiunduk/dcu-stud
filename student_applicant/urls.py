from django.urls import path, include

from student_applicant import views
from student_applicant.views import StudentApplicantDetailView, StudentApplicantUpdateView, StudentApplicantDeleteView, \
    ApplicantDocumentDetailView, ApplicantDocumentUpdateView, ApplicantDocumentUploadView

urlpatterns = [
    path('signup/<int:fk>/', views.StudentSignUpView.as_view(), name='signup-applicant'),
    path('create', views.StudentApplicantCreateView.as_view(), name='create-applicant'),
    path('<int:pk>/update/', StudentApplicantUpdateView.as_view(), name='student-applicant-update'),
    path('delete/<int:pk>/', StudentApplicantDeleteView.as_view(), name='student-applicant-delete'),
    path('<int:pk>/', StudentApplicantDetailView.as_view(), name='student-applicant-detail'),
    path('upload/<int:pk>', ApplicantDocumentUploadView.as_view(), name='document-applicant-upload'),
    path('document/<int:pk>/', ApplicantDocumentDetailView.as_view(), name='document-applicant-detail'),
    path('document/update/<int:pk>/', ApplicantDocumentUpdateView.as_view(), name='document-applicant-update'),
    path('document/delete/<int:pk>/', views.document_delete, name='document-applicant-delete'),
    path('announcement_list/<int:pk>/', views.applicant_announcements_list, name='applicant-announcements-list'),
    path('all_announcement_list/<int:pk>/', views.announcements_list, name='all-announcements-list'),
    path('announcement/detail/<int:pk>/', views.ApplicantAnnouncementDetailView.as_view(),
         name='student-applicant-announcement-detail'),
    path('request_change_status/<int:pk>/<int:fk>', views.request_change_status, name='student-applicant-announcement-change'),
    path('announcement_apply/<int:pk>/', views.apply_for_announcement, name='apply-for-announcement')

]