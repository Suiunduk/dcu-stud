from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from tablib import Dataset

from announcement.models import Announcement, AnnouncementDocument
from core.decorators import superuser_required
from core.models import ParentType, Gender, TypeOfApplying, EducationProgram, EducationForm, Status, Country
from student_applicant.models import StudentApplicant
from university_employee.models import Employee
from student_abroad.models import StudentAbroad
from student_foreign.models import StudentForeign
from university_local.models import University
from users.models import CustomUser


def homepage(request):
    if request.user.is_authenticated:
        user = request.user
        customUser = CustomUser.objects.get(id=user.id)

        if customUser.is_superuser:
            students_count = StudentAbroad.objects.all().count()
            universities_count = University.objects.all().count()
            employees_count = Employee.objects.all().count()
            return render(request, 'core/admin_homepage.html', {"students_count": students_count,
                                                                "universities_count": universities_count,
                                                                "employees_count": employees_count})

        elif customUser.user_type == 'university_employee':
            employee = Employee.objects.get(user_id=customUser.id)
            students_count_for_emp = StudentAbroad.objects.filter(edu_organisation=employee.edu_organisation).count()
            return render(request, 'core/employee_homepage.html', {"students_count": students_count_for_emp})

        elif customUser.user_type == 'student_applicant':
            if not StudentApplicant.objects.filter(user=customUser.id).exists():
                return redirect('create-applicant')
            return render(request, 'core/student_homepage.html')

        else:
            return render(request, 'core/student_homepage.html')

    else:
        students_count = StudentAbroad.objects.all().count()
        students_count_by_country = StudentAbroad.objects.all().values('education_country'). \
                                        annotate(count=Count('education_country')).order_by('-count')[:10]
        students_country_count = StudentAbroad.objects.values('education_country').distinct().count()
        abr_students_count = StudentForeign.objects.all().count()
        abr_students_count_by_country = StudentForeign.objects.all().values('country'). \
                                            annotate(count=Count('country')).order_by('-count')[:10]
        abr_students_count_by_uni = StudentForeign.objects.all().values('edu_organisation__org_name'). \
                                        annotate(count=Count('edu_organisation')).order_by('-count')[:10]
        abr_students_country_count = StudentForeign.objects.values('country').distinct().count()

        announcements = Announcement.objects.all()
        announcement_docs = AnnouncementDocument.objects.all()

        return render(request, 'core/landing/landing_page.html', {"students_count": students_count,
                                                                  "students_count_by_country":
                                                                      students_count_by_country,
                                                                  "students_country_count": students_country_count,
                                                                  "abr_students_count": abr_students_count,
                                                                  "abr_students_count_by_country":
                                                                      abr_students_count_by_country,
                                                                  "abr_students_count_by_uni":
                                                                      abr_students_count_by_uni,
                                                                  "abr_students_country_count":
                                                                      abr_students_country_count,
                                                                  "announcements": announcements,
                                                                  "announcement_docs": announcement_docs})


class AnnouncementDetailView(DetailView):
    model = Announcement
    template_name = "core/landing/announcement_landing.html"

    def get_context_data(self, **kwargs):
        context = super(AnnouncementDetailView, self).get_context_data(**kwargs)
        context['documents'] = AnnouncementDocument.objects.filter(announcement=self.kwargs['pk'])
        return context


@login_required
def parent_types_list(request):
    parent_types = ParentType.objects.all()
    return render(request, 'core/parent_types_list.html', {"parent_types": parent_types})


class ParentTypeCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = ParentType
    fields = '__all__'
    success_message = "Новая степень родства добавлена"

    def get_form(self, **kwargs):
        form = super(ParentTypeCreateView, self).get_form()
        return form


class ParentTypeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ParentType
    fields = '__all__'
    success_message = "Запись успешно обновлена"

    def get_form(self, **kwargs):
        form = super(ParentTypeUpdateView, self).get_form()
        return form


class ParentTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = ParentType
    success_url = reverse_lazy('parent-types-list')


@login_required
def genders_list(request):
    genders = Gender.objects.all()
    return render(request, 'core/genders_list.html', {"genders": genders})


class GenderCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Gender
    fields = '__all__'
    success_message = "Новый пол добавлен"

    def get_form(self, **kwargs):
        form = super(GenderCreateView, self).get_form()
        return form


class GenderUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Gender
    fields = '__all__'
    success_message = "Запись успешно обновлена"

    def get_form(self, **kwargs):
        form = super(GenderUpdateView, self).get_form()
        return form


class GenderDeleteView(LoginRequiredMixin, DeleteView):
    model = Gender
    success_url = reverse_lazy('genders-list')


@login_required
def types_of_applying_list(request):
    types_of_applying = TypeOfApplying.objects.all()
    return render(request, 'core/types_of_applying_list.html', {"types_of_applying": types_of_applying})


class TypeOfApplyingCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = TypeOfApplying
    fields = '__all__'
    success_message = "Новая линия поступления добавлена"

    def get_form(self, **kwargs):
        form = super(TypeOfApplyingCreateView, self).get_form()
        return form


class TypeOfApplyingUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TypeOfApplying
    fields = '__all__'
    success_message = "Запись успешно обновлена"

    def get_form(self, **kwargs):
        form = super(TypeOfApplyingUpdateView, self).get_form()
        return form


class TypeOfApplyingDeleteView(LoginRequiredMixin, DeleteView):
    model = TypeOfApplying
    success_url = reverse_lazy('types-of-applying-list')


@login_required
def education_programs_list(request):
    education_programs = EducationProgram.objects.all()
    return render(request, 'core/education_programs_list.html', {"education_programs": education_programs})


class EducationProgramCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = EducationProgram
    fields = '__all__'
    success_message = "Новая программа обучения добавлена"

    def get_form(self, **kwargs):
        form = super(EducationProgramCreateView, self).get_form()
        return form


class EducationProgramUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = EducationProgram
    fields = '__all__'
    success_message = "Запись успешно обновлена"

    def get_form(self, **kwargs):
        form = super(EducationProgramUpdateView, self).get_form()
        return form


class EducationProgramDeleteView(LoginRequiredMixin, DeleteView):
    model = EducationProgram
    success_url = reverse_lazy('education-programs-list')


@login_required
def education_forms_list(request):
    education_forms = EducationForm.objects.all()
    return render(request, 'core/education_forms_list.html', {"education_forms": education_forms})


class EducationFormCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = EducationForm
    fields = '__all__'
    success_message = "Новая форма обучения добавлена"

    def get_form(self, **kwargs):
        form = super(EducationFormCreateView, self).get_form()
        return form


class EducationFormUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = EducationForm
    fields = '__all__'
    success_message = "Запись успешно обновлена"

    def get_form(self, **kwargs):
        form = super(EducationFormUpdateView, self).get_form()
        return form


class EducationFormDeleteView(LoginRequiredMixin, DeleteView):
    model = EducationForm
    success_url = reverse_lazy('education-forms-list')


@login_required
def statuses_list(request):
    statuses = Status.objects.all()
    return render(request, 'core/statuses_list.html', {"statuses": statuses})


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    fields = '__all__'
    success_message = "Новый статус добавлен"

    def get_form(self, **kwargs):
        form = super(StatusCreateView, self).get_form()
        return form


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    fields = '__all__'
    success_message = "Запись успешно обновлена"

    def get_form(self, **kwargs):
        form = super(StatusUpdateView, self).get_form()
        return form


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    success_url = reverse_lazy('statuses-list')


@login_required
def countries_list(request):
    countries = Country.objects.all()
    return render(request, 'core/countries_list.html', {"countries": countries})


class CountryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Country
    fields = '__all__'
    success_message = "Новая страна добавлена"

    def get_form(self, **kwargs):
        form = super(CountryCreateView, self).get_form()
        return form


class CountryUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Country
    fields = '__all__'
    success_message = "Запись успешно обновлена"

    def get_form(self, **kwargs):
        form = super(CountryUpdateView, self).get_form()
        return form


class CountryDeleteView(LoginRequiredMixin, DeleteView):
    model = Country
    success_url = reverse_lazy('countries-list')


@superuser_required
def country_upload(request):
    if request.method == 'POST':
        dataset = Dataset()
        new_country = request.FILES['myfile']
        imported_data = dataset.load(new_country.read(), format='xlsx')
        print(imported_data)
        for data in imported_data:
            if data[1] is not None:
                value = Country(
                    data[0],
                    data[1],
                    data[2],
                    data[3],
                    data[4]
                )
                value.save()
        return redirect('countries-list')

    return render(request, 'core/countries_upload.html')

