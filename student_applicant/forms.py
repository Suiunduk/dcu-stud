from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from users.models import CustomUser


class StudentApplicantSignUpForm(UserCreationForm):
    lastname = forms.CharField(label='Фамилия', max_length=255)
    firstname = forms.CharField(label='Имя', max_length=255)

    email = forms.EmailField(label='Email', )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'last_name', 'first_name')

    @transaction.atomic
    def save(self):
        user = super(StudentApplicantSignUpForm, self).save(commit=False)
        user.user_type = 'student_applicant'
        user.username = self.cleaned_data.get('email')
        user.last_name = self.cleaned_data.get('lastname')
        user.first_name = self.cleaned_data.get('firstname')
        user.save()

        return user
