from django.urls import path

from announcement import views
from announcement.views import AnnouncementCreateView, AnnouncementDeleteView, AnnouncementDetailView, \
  AnnouncementUpdateView, DocumentUploadView, DocumentDetailView, DocumentUpdateView, AdditionalDocumentUpdateView, \
  AdditionalDocumentDetailView, AdditionalDocumentCreateView

urlpatterns = [
  path('list', views.announcement_list, name='announcement-list'),
  path('<int:pk>/', AnnouncementDetailView.as_view(), name='announcement-detail'),
  path('create/', AnnouncementCreateView.as_view(), name='announcement-create'),
  path('<int:pk>/update/', AnnouncementUpdateView.as_view(), name='announcement-update'),
  path('delete/<int:pk>/', AnnouncementDeleteView.as_view(), name='announcement-delete'),
  path('applicants_list/<int:pk>/', views.announcement_applicants_list, name='announcement-applicants-list'),
  path('applicant-reject/<int:pk>', views.reject_applicant, name='reject-applicant'),
  path('applicant-confirm/<int:pk>', views.confirm_applicant, name='confirm-applicant'),
  path('upload/<int:pk>', DocumentUploadView.as_view(), name='an-document-upload'),
  path('document/<int:pk>/', DocumentDetailView.as_view(), name='an-document-detail'),
  path('document/update/<int:pk>/', DocumentUpdateView.as_view(), name='an-document-update'),
  path('document/delete/<int:pk>/', views.document_delete, name='an-document-delete'),
  path('add_document/create/<int:pk>', AdditionalDocumentCreateView.as_view(), name='add-document-create'),
  path('add_document/<int:pk>/', AdditionalDocumentDetailView.as_view(), name='add-document-detail'),
  path('add_document/update/<int:pk>/', AdditionalDocumentUpdateView.as_view(), name='add-document-update'),
  path('add_document/delete/<int:pk>/', views.additional_document_delete, name='add-document-delete')
]
