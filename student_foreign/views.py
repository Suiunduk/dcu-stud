import xlrd
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from tablib import Dataset

from core.decorators import superuser_required, employee_required, super_or_emp_required
from university_employee.models import Employee
from student_foreign.forms import StudentAbroadCreateFormForEmp, StudentAbroadCreateForm, StudentAbroadUpdateForm
from student_foreign.models import StudentForeign
from university_local.models import University
from users.models import CustomUser


@method_decorator([login_required, superuser_required], name='dispatch')
class StudentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StudentForeign
    form_class = StudentAbroadCreateForm
    template_name = 'student_foreign/studentforeign_form.html'
    success_message = "Новый студент успешно добавлен"

    def get_form(self, **kwargs):
        form = super(StudentCreateView, self).get_form()
        form.fields['date_of_birth'].widget = widgets.DateInput(
            attrs={'type': 'date'})
        return form

    def form_valid(self, form):
        student = form.save()
        return redirect('student-foreign-detail', student.id)


@method_decorator([login_required, employee_required], name='dispatch')
class StudentCreateViewForEmp(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StudentForeign
    form_class = StudentAbroadCreateFormForEmp
    template_name = 'student_foreign/studentforeign_form.html'
    success_message = "Новый студент успешно добавлен"

    def get_form(self, **kwargs):
        form = super(StudentCreateViewForEmp, self).get_form()
        form.fields['date_of_birth'].widget = widgets.DateInput(
            attrs={'type': 'date'})
        return form

    def form_valid(self, form):
        form.university = University.objects.get(id=self.kwargs['fk'])
        student = form.save()
        return redirect('student-foreign-detail', student.id)


@super_or_emp_required
def student_list(request):
    user = request.user
    customUser = CustomUser.objects.get(pk=user.id)
    employee = None
    if customUser.is_employee:
        employee = Employee.objects.get(pk=user.id)
        students = StudentForeign.objects.filter(university=employee.university)
    else:
        students = StudentForeign.objects.all()
    return render(request, 'student_foreign/student_list.html', {"students": students, "employee": employee})


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = StudentForeign
    template_name = "student_foreign/student_detail.html"

    def get_context_data(self, **kwargs):
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        return context


class StudentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = StudentForeign
    form_class = StudentAbroadUpdateForm
    success_message = "Запись успешно обновлена"

    def get_form(self, **kwargs):
        form = super(StudentUpdateView, self).get_form()
        form.fields['date_of_birth'].widget = widgets.DateInput(format='%Y-%m-%d',
                                                                attrs={'type': 'date'})
        return form


@method_decorator([login_required, super_or_emp_required], name='dispatch')
class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = StudentForeign
    success_message = "Запись успешно удалена"
    success_url = reverse_lazy('student-foreign-list')

@employee_required
def student_upload(request):
    if request.method == 'POST':
        dataset = Dataset()
        new_students = request.FILES['myfile']
        employee = Employee.objects.get(pk=request.user.id)
        university = employee.university
        ethKyrg = False
        imported_data = dataset.load(new_students.read(), format='xlsx')
        print(imported_data)
        for data in imported_data:
            if data[1] is not None:
                if data[3] is not None and data[3] == 1:
                    ethKyrg = True
                else:
                    ethKyrg = False
                value = StudentForeign(
                    data[0],
                    data[1],
                    data[2],
                    ethKyrg,
                    data[4],
                    data[5],
                    university.id,
                    data[6],
                    data[7],
                    data[8],
                    data[9],
                    data[10],
                    data[11]
                )
                value.save()
        return redirect('student-foreign-list')

            # result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

        # if not result.has_errors():
        #    person_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'student_foreign/students_upload.html')

