from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from announcement.models import AnnouncementApplicants, Announcement, AnnouncementDocument, \
    AnnouncementAdditionalDocumentNames
from core.decorators import applicant_required, superuser_required
from student_abroad.forms import ConfirmForm
from student_applicant.forms import StudentApplicantSignUpForm, StudentApplicantCreateForm, StudentApplicantUpdateForm, \
    ApplicantDocumentUploadForm
from student_applicant.models import StudentApplicant, StudentApplicantParent, StudentApplicantDocuments
from users.models import CustomUser


class StudentSignUpView(CreateView):
    model = CustomUser
    form_class = StudentApplicantSignUpForm
    template_name = 'signup_applicant.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        context = super(StudentSignUpView, self).get_context_data(**kwargs)
        return context

    def get_form(self, **kwargs):
        form = super(StudentSignUpView, self).get_form()
        return form

    def form_valid(self, form):
        form.announcement = Announcement.objects.get(id=self.kwargs['fk'])
        user = form.save()
        login(self.request, user)
        return redirect('homepage')


@method_decorator([login_required, applicant_required], name='dispatch')
class StudentApplicantCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StudentApplicant
    form_class = StudentApplicantCreateForm
    template_name = 'student_applicant/studentapplicant_form.html'
    success_message = "Данные успешно добавлены"

    def get_context_data(self, **kwargs):
        context = super(StudentApplicantCreateView, self).get_context_data(**kwargs)
        context['template'] = 'base.html'
        return context

    def get_form(self, **kwargs):
        form = super(StudentApplicantCreateView, self).get_form()
        form.fields['date_of_birth'].widget = widgets.DateInput(
            attrs={'type': 'date'})
        form.fields['graduation_date'].widget = widgets.DateInput(
            attrs={'type': 'date'})
        return form

    def form_valid(self, form):
        user = self.request.user
        form.user = self.request.user
        form.lastname = self.request.user.last_name
        form.firstname = self.request.user.first_name
        form.email = self.request.user.email
        student = form.save()
        announcement_applicants = AnnouncementApplicants.objects.get(applicant=user)
        announcement_applicants.status = 'waiting'
        announcement_applicants.save()
        return redirect('student-applicant-detail', user.id)


class StudentApplicantDetailView(LoginRequiredMixin, DetailView):
    model = StudentApplicant
    template_name = "student_applicant/student_detail.html"

    def get_context_data(self, **kwargs):
        context = super(StudentApplicantDetailView, self).get_context_data(**kwargs)
        context['student_parents'] = StudentApplicantParent.objects.filter(student=self.kwargs['pk'])
        context['documents'] = StudentApplicantDocuments.objects.filter(student=self.kwargs['pk'])
        return context


class StudentApplicantUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = StudentApplicant
    form_class = StudentApplicantUpdateForm
    success_message = "Запись успешно обновлена"

    def get_context_data(self, **kwargs):
        context = super(StudentApplicantUpdateView, self).get_context_data(**kwargs)
        context['template'] = 'core/base.html'
        return context

    def get_form(self, **kwargs):
        form = super(StudentApplicantUpdateView, self).get_form()
        form.fields['date_of_birth'].widget = widgets.DateInput(format='%Y-%m-%d',
                                                                attrs={'type': 'date'})

        form.fields['graduation_date'].widget = widgets.DateInput(format='%Y-%m-%d',
                                                                  attrs={'type': 'date'})
        return form


@method_decorator([login_required, superuser_required], name='dispatch')
class StudentApplicantDeleteView(LoginRequiredMixin, DeleteView):
    model = StudentApplicant
    success_message = "Запись успешно удалена"
    success_url = reverse_lazy('homepage')


class ApplicantDocumentUploadView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StudentApplicantDocuments
    form_class = ApplicantDocumentUploadForm
    success_message = "Документ добавлен успешно"

    def get_form(self, **kwargs):
        form = super(ApplicantDocumentUploadView, self).get_form()
        return form

    def form_valid(self, form):
        student = StudentApplicant.objects.get(user_id=self.kwargs['pk'])
        form.student = student
        user = form.save()
        return redirect('student-applicant-detail', student.user_id)


class ApplicantDocumentDetailView(LoginRequiredMixin, DetailView):
    model = StudentApplicantDocuments
    template_name = "student_applicant/documentapplicant_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ApplicantDocumentDetailView, self).get_context_data(**kwargs)
        return context


class ApplicantDocumentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = StudentApplicantDocuments
    fields = ['name', 'description', 'file', ]
    success_message = "Документ успешно обновлен"

    def get_form(self, **kwargs):
        form = super(ApplicantDocumentUpdateView, self).get_form()
        return form


def document_delete(request, pk):
    student = None
    user = request.user
    customUser = CustomUser.objects.get(pk=user.id)
    if request.method == 'POST':
        document = StudentApplicantDocuments.objects.get(id=pk)
        student = document.student
        document.delete()
    return redirect('student-applicant-detail', student.user_id)


@applicant_required
def applicant_announcements_list(request, pk):
    applicant = StudentApplicant.objects.get(user_id=pk)
    announcement_applicants = AnnouncementApplicants.objects.filter(applicant=applicant.user)

    return render(request, 'student_applicant/applicant_announcements_list.html',
                  {"announcements": announcement_applicants})


@applicant_required
def announcements_list(request, pk):
    applicant = StudentApplicant.objects.get(user_id=pk)
    announcement_applicants = AnnouncementApplicants.objects.filter(applicant=applicant.user)
    announcements = Announcement.objects.filter(status='active')

    return render(request, 'student_applicant/announcements_list.html',
                  {"announcements": announcements})


class ApplicantAnnouncementDetailView(LoginRequiredMixin, DetailView):
    model = Announcement
    template_name = "student_applicant/applicant_announcement_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ApplicantAnnouncementDetailView, self).get_context_data(**kwargs)
        context['documents'] = AnnouncementDocument.objects.filter(announcement=self.kwargs['pk'])
        context['additional_docs'] = AnnouncementAdditionalDocumentNames.objects.filter(announcement=self.kwargs['pk'])
        return context


def request_change_status(request, pk):
    announcement_applicants = AnnouncementApplicants.objects.get(announcement_id=pk)
    announcement_applicants.status = 'waiting'
    announcement_applicants.save()
    return redirect('applicant-announcements-list', request.user.id)


def apply_for_announcement(request, pk):
    if request.method == 'POST':
        form = ConfirmForm(request.POST)
        user = request.user
        announcement = Announcement.objects.get(id=pk)
        announcement_applicant = AnnouncementApplicants.objects.filter(applicant=user, announcement=announcement)
        if form.is_valid():
            if announcement_applicant:
                messages.warning(request, 'Вы уже учавствуете на данном конкурсе!')
                return redirect('all-announcements-list', user.id)
            else:
                new_announcement_applicant = AnnouncementApplicants.objects.create(announcement=announcement,
                                                                                   applicant=user,
                                                                                   status='waiting')
                new_announcement_applicant.save()
                return redirect('applicant-announcements-list', user.id)
    else:
        form = ConfirmForm()

    return render(request, 'student_applicant/announcement_join.html', {'form': form})
