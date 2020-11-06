from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from edu_organisation.models import EduOrganisation
from university_employee.models import Employee
from student_abroad.models import StudentAbroad
from university_local.models import University
from users.models import CustomUser

edu_organisations = EduOrganisation.objects.all()


class EmployeeSignUpForm(UserCreationForm):
    lastname = forms.CharField(label='Фамилия', max_length=100)
    firstname = forms.CharField(label='Имя', max_length=100)
    fathersname = forms.CharField(label='Отчество', max_length=100, required=False)
    position = forms.CharField(label='Должность', max_length=100)
    phone_number = forms.CharField(label='Номер телефона', max_length=20)
    email = forms.EmailField(label='Email')
    edu_organisation = forms.ModelChoiceField(label='Учебное заведение', widget=forms.Select,
                                              queryset=edu_organisations, required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'lastname', 'firstname')

    @transaction.atomic
    def save(self):
        user = super(EmployeeSignUpForm, self).save(commit=False)
        user.user_type = 'university_employee'
        user.username = self.cleaned_data.get('email')
        user.save()
        employee = Employee.objects.create(user=user,
                                           lastname=self.cleaned_data.get('lastname'),
                                           firstname=self.cleaned_data.get('firstname'),
                                           fathersname=self.cleaned_data.get('fathersname'),
                                           position=self.cleaned_data.get('position'),
                                           phone_number=self.cleaned_data.get('phone_number'),
                                           email=self.cleaned_data.get('email'),
                                           edu_organisation=self.cleaned_data.get('edu_organisation'))
        return user


class EmployeeCreateForm(UserCreationForm):
    lastname = forms.CharField(label='Фамилия', max_length=100)
    firstname = forms.CharField(label='Имя', max_length=100)
    fathersname = forms.CharField(label='Отчество', max_length=100, required=False)
    position = forms.CharField(label='Должность', max_length=100)
    phone_number = forms.CharField(label='Номер телефона', max_length=20)
    email = forms.EmailField(label='Email')
    edu_organisation = forms.HiddenInput()

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'lastname', 'firstname')

    @transaction.atomic
    def save(self):
        user = super(EmployeeCreateForm, self).save(commit=False)
        user.user_type = 'university_employee'
        user.username = self.cleaned_data.get('email')
        user.save()
        employee = Employee.objects.create(user=user,
                                           lastname=self.cleaned_data.get('lastname'),
                                           firstname=self.cleaned_data.get('firstname'),
                                           fathersname=self.cleaned_data.get('fathersname'),
                                           position=self.cleaned_data.get('position'),
                                           phone_number=self.cleaned_data.get('phone_number'),
                                           email=self.cleaned_data.get('email'),
                                           edu_organisation=self.edu_organisation)
        return user


class EmployeeUpdateForm(forms.ModelForm):
    lastname = forms.CharField(label='Фамилия', max_length=100)
    firstname = forms.CharField(label='Имя', max_length=100)
    fathersname = forms.CharField(label='Отчество', max_length=100, required=False)
    position = forms.CharField(label='Должность', max_length=100)
    phone_number = forms.CharField(label='Номер телефона', max_length=20)
    email = forms.EmailField(label='Email')

    class Meta:
        model = Employee
        fields = ('lastname', 'firstname', 'fathersname', 'position', 'phone_number', 'email')
