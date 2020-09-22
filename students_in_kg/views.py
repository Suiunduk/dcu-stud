from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from core.decorators import superuser_required, employee_required, super_or_emp_required
from employees.models import Employee
from students_in_kg.forms import StudentAbroadCreateFormForEmp, StudentAbroadCreateForm
from students_in_kg.models import Student_abroad
from universities.models import University
from users.models import CustomUser


@method_decorator([login_required, superuser_required], name='dispatch')
class StudentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Student_abroad
    form_class = StudentAbroadCreateForm
    template_name = 'students_in_kg/student_abroad_form.html'
    success_message = "Новый студент успешно добавлен"

    def get_form(self, **kwargs):
        form = super(StudentCreateView, self).get_form()
        form.fields['date_of_birth'].widget = widgets.DateInput(
            attrs={'type': 'date'})
        return form

    def form_valid(self, form):
        student = form.save()
        return redirect('student-abroad-detail', student.id)


@method_decorator([login_required, employee_required], name='dispatch')
class StudentCreateViewForEmp(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Student_abroad
    form_class = StudentAbroadCreateFormForEmp
    template_name = 'students_in_kg/student_abroad_form.html'
    success_message = "Новый студент успешно добавлен"

    def get_form(self, **kwargs):
        form = super(StudentCreateViewForEmp, self).get_form()
        form.fields['date_of_birth'].widget = widgets.DateInput(
            attrs={'type': 'date'})
        return form

    def form_valid(self, form):
        form.university = University.objects.get(id=self.kwargs['fk'])
        student = form.save()
        return redirect('student-abroad-detail', student.id)


@super_or_emp_required
def student_list(request):
    user = request.user
    customUser = CustomUser.objects.get(pk=user.id)
    employee = None
    if customUser.is_employee:
        employee = Employee.objects.get(pk=user.id)
        students = Student_abroad.objects.filter(university=employee.university)
    else:
        students = Student_abroad.objects.all()
    return render(request, 'students_in_kg/student_list.html', {"students": students, "employee": employee})


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student_abroad
    template_name = "students_in_kg/student_detail.html"

    def get_context_data(self, **kwargs):
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        return context


class StudentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Student_abroad
    fields = "__all__"
    success_message = "Запись успешно обновлена"

    def get_form(self, **kwargs):
        form = super(StudentUpdateView, self).get_form()
        form.fields['date_of_birth'].widget = widgets.DateInput(format='%Y-%m-%d',
                                                                attrs={'type': 'date'})
        return form


@method_decorator([login_required, super_or_emp_required], name='dispatch')
class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student_abroad
    success_url = reverse_lazy('student-abroad-list')
