from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView

from announcement.forms import DocumentUploadForm
from announcement.models import Announcement, AnnouncementDocument


@login_required
def announcement_list(request):
    announcements = Announcement.objects.all()
    return render(request, 'announcement/announcement_list.html', {"announcements": announcements})


class AnnouncementDetailView(LoginRequiredMixin, DetailView):
    model = Announcement
    template_name = "announcement/announcement_detail.html"

    def get_context_data(self, **kwargs):
        context = super(AnnouncementDetailView, self).get_context_data(**kwargs)
        context['documents'] = AnnouncementDocument.objects.filter(announcement=self.kwargs['pk'])
        return context


class AnnouncementCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Announcement
    fields = '__all__'
    success_message = _("Новая программа успешно добавлена")

    def get_form(self, **kwargs):
        form = super(AnnouncementCreateView, self).get_form()
        return form


class AnnouncementUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Announcement
    fields = '__all__'
    success_message = _("Запись успешно обновлена")

    def get_form(self, **kwargs):
        form = super(AnnouncementUpdateView, self).get_form()
        return form


class AnnouncementDeleteView(LoginRequiredMixin, DeleteView):
    model = Announcement
    success_url = reverse_lazy('announcement-list')


class DocumentUploadView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AnnouncementDocument
    form_class = DocumentUploadForm
    success_message = "Документ добавлен успешно"

    def get_form(self, **kwargs):
        form = super(DocumentUploadView, self).get_form()
        return form

    def form_valid(self, form):
        announcement = Announcement.objects.get(id=self.kwargs['pk'])
        form.announcement = announcement
        user = form.save()
        return redirect('announcement-detail', announcement.id)


class DocumentDetailView(LoginRequiredMixin, DetailView):
    model = AnnouncementDocument
    template_name = "announcement/announcement_document_detail.html"

    def get_context_data(self, **kwargs):
        context = super(DocumentDetailView, self).get_context_data(**kwargs)
        return context


class DocumentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AnnouncementDocument
    fields = ['name', 'description', 'file', ]
    success_message = "Документ успешно обновлен"

    def get_form(self, **kwargs):
        form = super(DocumentUpdateView, self).get_form()
        return form


def document_delete(request, pk):
    user = request.user
    if request.method == 'POST':
        document = AnnouncementDocument.objects.get(id=pk)
        announcement = document.announcement
        document.delete()
    return redirect('announcement-detail', announcement.id)
