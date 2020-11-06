from django.urls import path

from announcement import views
from announcement.views import AnnouncementCreateView, AnnouncementDeleteView, AnnouncementDetailView, \
  AnnouncementUpdateView, DocumentUploadView, DocumentDetailView, DocumentUpdateView

urlpatterns = [
  path('list', views.announcement_list, name='announcement-list'),
  path('<int:pk>/', AnnouncementDetailView.as_view(), name='announcement-detail'),
  path('create/', AnnouncementCreateView.as_view(), name='announcement-create'),
  path('<int:pk>/update/', AnnouncementUpdateView.as_view(), name='announcement-update'),
  path('delete/<int:pk>/', AnnouncementDeleteView.as_view(), name='announcement-delete'),
  path('upload/<int:pk>', DocumentUploadView.as_view(), name='an-document-upload'),
  path('document/<int:pk>/', DocumentDetailView.as_view(), name='an-document-detail'),
  path('document/update/<int:pk>/', DocumentUpdateView.as_view(), name='an-document-update'),
  path('document/delete/<int:pk>/', views.document_delete, name='an-document-delete')
]
