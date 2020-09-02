from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from employees.models import Employee
from students.models import Student
from universities.models import University
from users.models import CustomUser

universities = University.objects.all()


class EmployeeSignUpForm(UserCreationForm):
    lastname = forms.CharField(label='Фамилия', max_length=100)
    firstname = forms.CharField(label='Имя', max_length=100)
    fathersname = forms.CharField(label='Отчество', max_length=100, required=False)
    phone_number = forms.CharField(label='Номер телефона', max_length=20)
    email = forms.EmailField(label='Email')
    university = forms.ModelChoiceField(label='Университет', widget=forms.Select, queryset=universities, required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'lastname', 'firstname')

    @transaction.atomic
    def save(self):
        user = super(EmployeeSignUpForm, self).save(commit=False)
        user.is_employee = True
        user.username = self.cleaned_data.get('email')
        user.save()
        employee = Employee.objects.create(user=user,
                                           lastname=self.cleaned_data.get('lastname'),
                                           firstname=self.cleaned_data.get('firstname'),
                                           fathersname=self.cleaned_data.get('fathersname'),
                                           phone_number=self.cleaned_data.get('phone_number'),
                                           email=self.cleaned_data.get('email'),
                                           university=self.cleaned_data.get('university'))
        return user


class EmployeeCreateForm(UserCreationForm):
    lastname = forms.CharField(label='Фамилия', max_length=100)
    firstname = forms.CharField(label='Имя', max_length=100)
    fathersname = forms.CharField(label='Отчество', max_length=100, required=False)
    phone_number = forms.CharField(label='Номер телефона', max_length=20)
    email = forms.EmailField(label='Email')
    university = forms.HiddenInput()

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'lastname', 'firstname')

    @transaction.atomic
    def save(self):
        user = super(EmployeeCreateForm, self).save(commit=False)
        user.is_employee = True
        user.username = self.cleaned_data.get('email')
        user.save()
        employee = Employee.objects.create(user=user,
                                           lastname=self.cleaned_data.get('lastname'),
                                           firstname=self.cleaned_data.get('firstname'),
                                           fathersname=self.cleaned_data.get('fathersname'),
                                           phone_number=self.cleaned_data.get('phone_number'),
                                           email=self.cleaned_data.get('email'),
                                           university=self.university)
        return user


class EmployeeUpdateForm(forms.ModelForm):
    lastname = forms.CharField(label='Фамилия', max_length=100)
    firstname = forms.CharField(label='Имя', max_length=100)
    fathersname = forms.CharField(label='Отчество', max_length=100, required=False)
    phone_number = forms.CharField(label='Номер телефона', max_length=20)
    email = forms.EmailField(label='Email')

    class Meta:
        model = Employee
        fields = ('lastname', 'firstname', 'fathersname', 'phone_number', 'email')
