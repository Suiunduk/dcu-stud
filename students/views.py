from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView

from students.forms import StudentSignUpForm
from users.models import CustomUser


class StudentSignUpView(CreateView):
    model = CustomUser
    form_class = StudentSignUpForm
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('homepage')
