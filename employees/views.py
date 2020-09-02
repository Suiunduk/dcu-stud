from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from employees.forms import EmployeeSignUpForm, EmployeeCreateForm, EmployeeUpdateForm
from employees.models import Employee
from universities.models import University
from users.models import CustomUser
from core.decorators import superuser_required, super_or_emp_required


class EmployeeSignUpView(CreateView):
    model = CustomUser
    form_class = EmployeeSignUpForm
    template_name = 'signup_emp.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'employee'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('homepage')


@method_decorator([login_required, superuser_required], name='dispatch')
class EmployeeCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = EmployeeCreateForm
    template_name = 'employees/employee_form.html'
    success_message = "Новый сотрудник успешно добавлен"

    def get_context_data(self, **kwargs):
            kwargs['user_type'] = 'employee'
            return super().get_context_data(**kwargs)

    def get_form(self, **kwargs):
        form = super(EmployeeCreateView, self).get_form()
        return form

    def form_valid(self, form):
        university = University.objects.get(id=self.kwargs['fk'])
        form.university = university
        user = form.save()
        return redirect('employee-detail', user.id)


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = "employees/employee_detail.html"

    def get_context_data(self, **kwargs):
        context = super(EmployeeDetailView, self).get_context_data(**kwargs)
        return context


class EmployeeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Employee
    form_class = EmployeeUpdateForm
    success_message = "Запись успешно обновлена"

    def get_form(self, **kwargs):
        form = super(EmployeeUpdateView, self).get_form()
        return form


@method_decorator([login_required, superuser_required], name='dispatch')
class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    model = Employee
    success_url = reverse_lazy('universities-list')
