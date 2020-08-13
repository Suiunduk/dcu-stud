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
    lastname = forms.CharField(max_length=100)
    firstname = forms.CharField(max_length=100)
    fathersname = forms.CharField(max_length=100, required=False)
    phone_number = forms.CharField(max_length=20)
    email = forms.EmailField()
    university = forms.ModelChoiceField(widget=forms.Select, queryset=universities, required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'lastname', 'firstname')

    @transaction.atomic
    def save(self):
        user = super(EmployeeSignUpForm, self).save(commit=False)
        user.is_student = True
        user.save()
        employee = Employee.objects.create(user=user,
                                           lastname=self.cleaned_data.get('lastname'),
                                           firstname=self.cleaned_data.get('firstname'),
                                           fathersname=self.cleaned_data.get('fathersname'),
                                           phone_number=self.cleaned_data.get('phone_number'),
                                           email=self.cleaned_data.get('email'),
                                           university=self.cleaned_data.get('university'))
        return user
