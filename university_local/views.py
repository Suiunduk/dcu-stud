import csv

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


from university_employee.models import Employee
from university_local.models import University
from university_local.resources import UniversityResource


@login_required
def university_list(request):
    universities = University.objects.all()
    return render(request, 'university_local/university_list.html', {"universities": universities})


class UniversityDetailView(LoginRequiredMixin, DetailView):
    model = University
    template_name = "university_local/university_detail.html"

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


# class UniversityBulkUploadView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
#     model = UniversityBulkUpload
#     template_name = 'university_local/universities_upload.html'
#     fields = ['csv_file']
#     success_url = '/university_local/list'
#     success_message = 'Университеты успешно добавлены'


@login_required
def downloadcsv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="university_template.csv"'

    writer = csv.writer(response)
    writer.writerow(['university_name', 'university_address'])

    return response


def simple_upload(request):
    if request.method == 'POST':
        university_resource = UniversityResource()
        dataset = Dataset()
        new_universities = request.FILES['myfile']

        imported_data = dataset.load(new_universities.read(), format='xlsx')
        print(imported_data)
        for data in imported_data:
            #print(data[1])
            value = University(
                data[0],
                data[1],
                data[2]
            )
            value.save()

            # result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

        # if not result.has_errors():
        #    person_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'core/uni_upload.html')
