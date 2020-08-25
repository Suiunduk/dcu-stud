from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from employees.models import Employee
from universities.models import University

@login_required
def university_list(request):
    universities = University.objects.all()
    return render(request, 'universities/university_list.html', {"universities": universities})


class UniversityDetailView(LoginRequiredMixin, DetailView):
    model = University
    template_name = "universities/university_detail.html"

    def get_context_data(self, **kwargs):
        context = super(UniversityDetailView, self).get_context_data(**kwargs)
        context['employees'] = Employee.objects.filter(university=self.kwargs['pk'])
        return context


class UniversityCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = University
    fields = '__all__'
    success_message = "Новый университет успешно добавлен"

    def get_form(self, **kwargs):
        form = super(UniversityCreateView, self).get_form()
        return form


class UniversityUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = University
    fields = '__all__'
    success_message = "Запись успешно обновлена"

    def get_form(self, **kwargs):
        form = super(UniversityUpdateView, self).get_form()
        return form


class UniversityDeleteView(LoginRequiredMixin, DeleteView):
    model = University
    success_url = reverse_lazy('universities-list')
