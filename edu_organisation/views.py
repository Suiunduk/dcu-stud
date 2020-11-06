from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from tablib import Dataset
from django.utils.translation import gettext as _

from django.contrib.auth.decorators import login_required
from edu_organisation.models import EduOrganisation
from university_employee.models import Employee


@login_required
def organisation_list(request):
    edu_organisations = EduOrganisation.objects.all()
    schools = EduOrganisation.objects.filter(org_type='school')
    colleges = EduOrganisation.objects.filter(org_type='college')
    lyceums = EduOrganisation.objects.filter(org_type='lyceum')
    universities = EduOrganisation.objects.filter(org_type='university')
    return render(request, 'edu_organisation/eduorganisation_list.html', {"organisations": edu_organisations, "schools":schools, "colleges": colleges, "lyceums": lyceums, "universities": universities})


class OrganisationDetailView(LoginRequiredMixin, DetailView):
    model = EduOrganisation
    template_name = "edu_organisation/eduorganisation_detail.html"

    def get_context_data(self, **kwargs):
        context = super(OrganisationDetailView, self).get_context_data(**kwargs)
        context['employees'] = Employee.objects.filter(edu_organisation=self.kwargs['pk'])
        return context


class OrganisationCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = EduOrganisation
    fields = '__all__'
    success_message = _("Новая организация успешно добавлена")

    def get_form(self, **kwargs):
        form = super(OrganisationCreateView, self).get_form()
        return form


class OrganisationUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = EduOrganisation
    fields = '__all__'
    success_message = _("Запись успешно обновлена")

    def get_form(self, **kwargs):
        form = super(OrganisationUpdateView, self).get_form()
        return form


class OrganisationDeleteView(LoginRequiredMixin, DeleteView):
    model = EduOrganisation
    success_url = reverse_lazy('organisations-list')
