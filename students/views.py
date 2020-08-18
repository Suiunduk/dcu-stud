from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView, DetailView, UpdateView, DeleteView

from core.decorators import employee_required
from students.forms import StudentSignUpForm, StudentCreateForm
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


class StudentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = CustomUser
    success_message = "New student successfully added."
    form_class = StudentCreateForm
    template_name = 'students/student_form.html'

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
        login(self.request, user)
        return redirect('homepage')



#@method_decorator([login_required, employee_required], name='dispatch')
@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {"students": students})


#@method_decorator([login_required, employee_required], name='dispatch')
class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = "students/student_detail.html"

    def get_context_data(self, **kwargs):
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        return context



#@method_decorator([login_required], name='dispatch')
class StudentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Student
    fields = '__all__'
    success_message = "Record successfully updated."

    def get_form(self, **kwargs):
        form = super(StudentUpdateView, self).get_form()

        # form.fields['passport'].widget = widgets.FileInput()
        return form


#@method_decorator([login_required], name='dispatch')
class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    success_url = reverse_lazy('student-list')

###VIEWS FOR STUDENT ACCESS###

class StudentProfileView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = "students/student_profile.html"

    def get_context_data(self, **kwargs):
        context = super(StudentProfileView, self).get_context_data(**kwargs)
        return context