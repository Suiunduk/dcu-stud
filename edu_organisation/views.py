from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

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

from core.decorators import superuser_required
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


@superuser_required
def edu_org_upload(request):
    if request.method == 'POST':
        dataset = Dataset()
        new_orgs = request.FILES['myfile']
        imported_data = dataset.load(new_orgs.read(), format='xlsx')
        org_type = None
        for data in imported_data:
            if data[1] is not None:
                if data[4] is not None and data[4] == 1:
                    org_type = 'school'
                elif data[4] is not None and data[4] == 2:
                    org_type = 'college'
                elif data[4] is not None and data[4] == 3:
                    org_type = 'lyceum'
                elif data[4] is not None and data[4] == 2:
                    org_type = 'university'

                value = EduOrganisation(
                    data[0],
                    data[1],
                    data[2],
                    data[3],
                    data[4]
                )
                value.save()
        return redirect('organisations-list')

    return render(request, 'edu_organisation/eduorganisations_upload.html')

