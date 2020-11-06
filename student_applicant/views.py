from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from student_applicant.forms import StudentApplicantSignUpForm
from users.models import CustomUser


class StudentSignUpView(CreateView):
    model = CustomUser
    form_class = StudentApplicantSignUpForm
    template_name = 'signup_applicant.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        context = super(StudentSignUpView, self).get_context_data(**kwargs)
        return context

    def get_form(self, **kwargs):
        form = super(StudentSignUpView, self).get_form()
        return form

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('homepage')

#
# @method_decorator([login_required, superuser_required], name='dispatch')
# class StudentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
#     model = CustomUser
#     form_class = StudentCreateForm
#     template_name = 'student_abroad/studentabroad_form.html'
#     success_message = "Новый студент успешно добавлен"
#
#     def get_context_data(self, **kwargs):
#         kwargs['user_type'] = 'student'
#         return super().get_context_data(**kwargs)
#
#     def get_form(self, **kwargs):
#         form = super(StudentCreateView, self).get_form()
#         form.fields['date_of_birth'].widget = widgets.DateInput(
#             attrs={'type': 'date'})
#         form.fields['year_of_applying'].widget = widgets.DateInput(
#             attrs={'type': 'date'})
#         return form
#
#     def form_valid(self, form):
#         user = form.save()
#         return redirect('student-detail', user.id)
#
#
# @method_decorator([login_required, employee_required], name='dispatch')
# class StudentCreateViewForEmp(LoginRequiredMixin, SuccessMessageMixin, CreateView):
#     model = CustomUser
#     form_class = StudentCreateFormForEmp
#     template_name = 'student_abroad/studentabroad_form.html'
#     success_message = "Новый студент успешно добавлен"
#
#     def get_context_data(self, **kwargs):
#         kwargs['user_type'] = 'student'
#         return super().get_context_data(**kwargs)
#
#     def get_form(self, **kwargs):
#         form = super(StudentCreateViewForEmp, self).get_form()
#         form.fields['date_of_birth'].widget = widgets.DateInput(
#             attrs={'type': 'date'})
#         form.fields['year_of_applying'].widget = widgets.DateInput(
#             attrs={'type': 'date'})
#         return form
#
#     def form_valid(self, form):
#         form.edu_organisation = EduOrganisation.objects.get(id=self.kwargs['fk'])
#         user = form.save()
#         return redirect('student-detail', user.id)
#
#
# @super_or_emp_required
# def student_list(request):
#     user = request.user
#     customUser = CustomUser.objects.get(pk=user.id)
#     employee = None
#     if customUser.user_type == 'university_employee':
#         employee = Employee.objects.get(pk=user.id)
#         students = StudentAbroad.objects.filter(edu_organisation=employee.edu_organisation)
#     else:
#         students = StudentAbroad.objects.all()
#     return render(request, 'student_abroad/student_list.html', {"students": students, "employee": employee})
#
#
# class StudentDetailView(LoginRequiredMixin, DetailView):
#     model = StudentAbroad
#     template_name = "student_abroad/student_detail.html"
#
#     def get_context_data(self, **kwargs):
#         context = super(StudentDetailView, self).get_context_data(**kwargs)
#         context['documents'] = StudentDocuments.objects.filter(student=self.kwargs['pk'])
#         context['phone_numbers'] = StudentPhoneNumber.objects.filter(student=self.kwargs['pk'])
#         context['student_parents'] = StudentParent.objects.filter(student=self.kwargs['pk'])
#         return context
#
#
# class StudentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
#     model = StudentAbroad
#     form_class = StudentUpdateForm
#     success_message = "Запись успешно обновлена"
#
#     def get_form(self, **kwargs):
#         form = super(StudentUpdateView, self).get_form()
#         form.fields['date_of_birth'].widget = widgets.DateInput(format='%Y-%m-%d',
#                                                                 attrs={'type': 'date'})
#         form.fields['year_of_applying'].widget = widgets.DateInput(format='%Y-%m-%d',
#                                                                    attrs={'type': 'date'})
#         return form
#
#
# @method_decorator([login_required, super_or_emp_required], name='dispatch')
# class StudentDeleteView(LoginRequiredMixin, DeleteView):
#     model = StudentAbroad
#     success_url = reverse_lazy('student-list')
#
#
# class DocumentUploadView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
#     model = StudentDocuments
#     form_class = DocumentUploadForm
#     success_message = "Документ добавлен успешно"
#
#     def get_form(self, **kwargs):
#         form = super(DocumentUploadView, self).get_form()
#         return form
#
#     def form_valid(self, form):
#         student = StudentAbroad.objects.get(user_id=self.kwargs['pk'])
#         form.student = student
#         user = form.save()
#         return redirect('student-detail', student.user_id)
#
#
# class DocumentDetailView(LoginRequiredMixin, DetailView):
#     model = StudentDocuments
#     template_name = "student_abroad/document_detail.html"
#
#     def get_context_data(self, **kwargs):
#         context = super(DocumentDetailView, self).get_context_data(**kwargs)
#         return context
#
#
# class DocumentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
#     model = StudentDocuments
#     fields = ['name', 'description', 'file', ]
#     success_message = "Документ успешно обновлен"
#
#     def get_form(self, **kwargs):
#         form = super(DocumentUpdateView, self).get_form()
#         return form
#
#
# def document_delete(request, pk):
#     user = request.user
#     customUser = CustomUser.objects.get(pk=user.id)
#     if request.method == 'POST':
#         document = StudentDocuments.objects.get(id=pk)
#         student = document.student
#         document.delete()
#     return redirect('student-detail', student.user_id)
