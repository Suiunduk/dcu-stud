from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from employees.forms import EmployeeSignUpForm
from users.models import CustomUser


class EmployeeSignUpView(CreateView):
    model = CustomUser
    form_class = EmployeeSignUpForm
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'employee'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('homepage')