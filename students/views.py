from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail, BadHeaderError
from django.forms import widgets
from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView, DetailView, UpdateView, DeleteView

from core.decorators import employee_required, superuser_required, super_or_emp_required, student_required
from dcu import settings
from dcu.resources import StudentResource
from students.forms import StudentSignUpForm, StudentCreateForm, StudentUpdateForm, ContactForm
from students.models import Student
from users.models import CustomUser


class StudentSignUpView(CreateView):
    model = CustomUser
    form_class = StudentSignUpForm
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def get_form(self, **kwargs):
        form = super(StudentSignUpView, self).get_form()
        form.fields['date_of_birth'].widget = widgets.DateInput(
            attrs={'type': 'date'})
        form.fields['year_of_applying'].widget = widgets.DateInput(
            attrs={'type': 'date'})
        return form

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('homepage')


@method_decorator([login_required, super_or_emp_required], name='dispatch')
class StudentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = StudentCreateForm
    template_name = 'students/student_form.html'
    success_message = "Новый студент успешно добавлен"

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def get_form(self, **kwargs):
        form = super(StudentCreateView, self).get_form()
        form.fields['date_of_birth'].widget = widgets.DateInput(
            attrs={'type': 'date'})
        form.fields['year_of_applying'].widget = widgets.DateInput(
            attrs={'type': 'date'})
        return form

    def form_valid(self, form):
        user = form.save()
        return redirect('student-detail', user.id)


@super_or_emp_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {"students": students})


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = "students/student_detail.html"

    def get_context_data(self, **kwargs):
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        return context


class StudentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Student
    form_class = StudentUpdateForm
    success_message = "Запись успешно обновлена"

    def get_form(self, **kwargs):
        form = super(StudentUpdateView, self).get_form()
        return form


@method_decorator([login_required, super_or_emp_required], name='dispatch')
class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    success_url = reverse_lazy('student-list')


@method_decorator([login_required, student_required], name='dispatch')
class StudentProfileView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = "students/student_profile.html"

    def get_context_data(self, **kwargs):
        context = super(StudentProfileView, self).get_context_data(**kwargs)
        return context


@student_required
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        # Если форма заполнена корректно, сохраняем все введённые пользователем значения
        if form.is_valid():
            subject = form.cleaned_data['subject']
            sender = form.cleaned_data['sender']
            message = 'Сообщение от ' + form.cleaned_data['sender'] + '\n \n' + form.cleaned_data['message']
            copy = form.cleaned_data['copy']

            recipients = [settings.EMAIL_HOST_USER]
            # Если пользователь захотел получить копию себе, добавляем его в список получателей
            if copy:
                recipients.append(sender)
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, recipients)
            except BadHeaderError:  # Защита от уязвимости
                return HttpResponse('Invalid header found')
            # Переходим на другую страницу, если сообщение отправлено
            return render(request, 'students/email_success.html')
    else:
        # Заполняем форму
        form = ContactForm()
    # Отправляем форму на страницу
    return render(request, 'students/send_email.html', {'form': form, 'username': auth.get_user(request).username})


def email_success(reguest):
    message = 'Ваше сообщение отправлено успешно!'
    return render(reguest, 'students/email_success.html', {'message': message})


def export_data(request):
    if request.method == 'POST':
        # Get selected option from form
        file_format = request.POST['file-format']
        student_resource = StudentResource()
        dataset = student_resource.export()
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
            return response
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="exported_data.json"'
            return response
        elif file_format == 'XLS(Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="exported_data.xls"'
            return response

    return render(request, 'students/students_export.html')
