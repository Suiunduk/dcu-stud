from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView

from announcement.forms import DocumentUploadForm, AdditionalDocumentCreateForm, RejectForm
from announcement.models import Announcement, AnnouncementDocument, AnnouncementAdditionalDocumentNames, \
    AnnouncementApplicants
from core.decorators import superuser_required


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
        context['additional_docs'] = AnnouncementAdditionalDocumentNames.objects.filter(announcement=self.kwargs['pk'])
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
    announcement = None
    user = request.user
    if request.method == 'POST':
        document = AnnouncementDocument.objects.get(id=pk)
        announcement = document.announcement
        document.delete()
    return redirect('announcement-detail', announcement.id)


class AdditionalDocumentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AnnouncementAdditionalDocumentNames
    form_class = AdditionalDocumentCreateForm
    success_message = "Документ добавлен успешно"

    def get_form(self, **kwargs):
        form = super(AdditionalDocumentCreateView, self).get_form()
        return form

    def form_valid(self, form):
        announcement = Announcement.objects.get(id=self.kwargs['pk'])
        form.announcement = announcement
        user = form.save()
        return redirect('announcement-detail', announcement.id)


class AdditionalDocumentDetailView(LoginRequiredMixin, DetailView):
    model = AnnouncementAdditionalDocumentNames
    template_name = "announcement/announcement_announcementadditionaldocumentnames_detail.html"

    def get_context_data(self, **kwargs):
        context = super(AdditionalDocumentDetailView, self).get_context_data(**kwargs)
        return context


class AdditionalDocumentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AnnouncementAdditionalDocumentNames
    fields = ['name', 'description', ]
    success_message = "Документ успешно обновлен"

    def get_form(self, **kwargs):
        form = super(AdditionalDocumentUpdateView, self).get_form()
        return form


def additional_document_delete(request, pk):
    announcement = None
    user = request.user
    if request.method == 'POST':
        document = AnnouncementAdditionalDocumentNames.objects.get(id=pk)
        announcement = document.announcement
        document.delete()
    return redirect('announcement-detail', announcement.id)


@superuser_required
def announcement_applicants_list(request, pk):
    announcement = Announcement.objects.get(id=pk)
    announcement_applicants = AnnouncementApplicants.objects.filter(announcement=announcement)

    return render(request, 'announcement/announcement_applicants_list.html', {"applicants": announcement_applicants})


def reject_applicant(request, pk):
    if request.method == 'POST':
        form = RejectForm(request.POST)
        if form.is_valid():
            announcement_applicants = AnnouncementApplicants.objects.get(id=pk)
            rejection_reason = request.POST.get('rejection_reason')
            announcement_applicants.status = 'not_confirmed'
            announcement_applicants.rejection_reason = rejection_reason
            announcement_applicants.save()
            return redirect('announcement-applicants-list', announcement_applicants.announcement.id)
    else:
        form = RejectForm()
    return render(request, 'announcement/announcement_applicants_reject.html', {'form': form})


def confirm_applicant(request, pk):
    announcement_applicants = AnnouncementApplicants.objects.get(id=pk)
    announcement_applicants.status = 'confirmed'
    announcement_applicants.save()
    return redirect('announcement-applicants-list', announcement_applicants.announcement.id)