from django import forms
from django.db import transaction

from edu_organisation.models import EduOrganisation
from student_foreign.models import StudentForeign
from university_local.models import University

edu_organisations = EduOrganisation.objects.all()

DEGREE = [
    ('bachelor', 'Бакалавриат'),
    ('master', 'Магистратура'),
    ('speciality', 'Специалитет'),
    ('other', 'Прочее')
]

EDU_TYPE = [
    ('och', 'Очная'),
    ('zaoch', 'Заочная')
]

class StudentAbroadCreateForm(forms.ModelForm):
    full_name = forms.CharField(label='Ф.И.О', max_length=255)
    country = forms.CharField(label='Гражданство', max_length=255)
    ethnical_kyrgyz = forms.BooleanField(label='Этнический кыргыз', required=False)
    education_type = forms.ChoiceField(label='Форма обучения', choices=EDU_TYPE)
    date_of_birth = forms.DateField(label='Дата рождения')
    edu_organisation = forms.ModelChoiceField(label='Место обучения', widget=forms.Select, queryset=edu_organisations)
    department = forms.CharField(label='Факультет/кафедра', max_length=255)
    speciality = forms.CharField(label='Программа/направление', max_length=255)
    degree = forms.ChoiceField(label='Обучение на квалификацию', choices=DEGREE)
    passport_number = forms.CharField(label='Серия и номер паспорта', max_length=255)
    phone_number = forms.CharField(label='Контактный номер', max_length=255)
    address = forms.CharField(label='Фактический адрес проживания в КР', max_length=255)

    class Meta:
        model = StudentForeign
        fields = ('full_name', 'country', 'ethnical_kyrgyz', 'education_type', 'date_of_birth', 'edu_organisation',
                  'department', 'speciality', 'degree', 'passport_number', 'phone_number', 'address')

    @transaction.atomic
    def save(self):
        student = StudentForeign.objects.create(full_name=self.cleaned_data.get('full_name'),
                                                country=self.cleaned_data.get('country'),
                                                ethnical_kyrgyz=self.cleaned_data.get('ethnical_kyrgyz'),
                                                education_type=self.cleaned_data.get('education_type'),
                                                date_of_birth=self.cleaned_data.get('date_of_birth'),
                                                edu_organisation=self.cleaned_data.get('edu_organisation'),
                                                department=self.cleaned_data.get('department'),
                                                speciality=self.cleaned_data.get('speciality'),
                                                degree=self.cleaned_data.get('degree'),
                                                passport_number=self.cleaned_data.get('passport_number'),
                                                phone_number=self.cleaned_data.get('phone_number'),
                                                address=self.cleaned_data.get('address'))

        return student


class StudentAbroadCreateFormForEmp(forms.ModelForm):
    full_name = forms.CharField(label='Ф.И.О', max_length=255)
    country = forms.CharField(label='Гражданство', max_length=255)
    ethnical_kyrgyz = forms.BooleanField(label='Этнический кыргыз', required=False)
    education_type = forms.ChoiceField(label='Форма обучения', choices=EDU_TYPE)
    date_of_birth = forms.DateField(label='Дата рождения')
    edu_organisation = forms.HiddenInput()
    department = forms.CharField(label='Факультет/кафедра', max_length=255)
    speciality = forms.CharField(label='Программа/направление', max_length=255)
    degree = forms.ChoiceField(label='Обучение на квалификацию', choices=DEGREE)
    passport_number = forms.CharField(label='Серия и номер паспорта', max_length=255)
    phone_number = forms.CharField(label='Контактный номер', max_length=255)
    address = forms.CharField(label='Фактический адрес проживания в КР', max_length=255)

    class Meta:
        model = StudentForeign
        fields = ('full_name', 'country', 'ethnical_kyrgyz', 'education_type', 'date_of_birth',
                  'department', 'speciality', 'degree', 'passport_number', 'phone_number', 'address')

    @transaction.atomic
    def save(self):
        student = StudentForeign.objects.create(full_name=self.cleaned_data.get('full_name'),
                                                country=self.cleaned_data.get('country'),
                                                ethnical_kyrgyz=self.cleaned_data.get('ethnical_kyrgyz'),
                                                education_type=self.cleaned_data.get('education_type'),
                                                date_of_birth=self.cleaned_data.get('date_of_birth'),
                                                edu_organisation=self.edu_organisation,
                                                department=self.cleaned_data.get('department'),
                                                speciality=self.cleaned_data.get('speciality'),
                                                degree=self.cleaned_data.get('degree'),
                                                passport_number=self.cleaned_data.get('passport_number'),
                                                phone_number=self.cleaned_data.get('phone_number'),
                                                address=self.cleaned_data.get('address'))

        return student


class StudentAbroadUpdateForm(forms.ModelForm):
    full_name = forms.CharField(label='Ф.И.О', max_length=255)
    country = forms.CharField(label='Гражданство', max_length=255)
    ethnical_kyrgyz = forms.BooleanField(label='Этнический кыргыз', required=False)
    education_type = forms.ChoiceField(label='Форма обучения', choices=EDU_TYPE)
    date_of_birth = forms.DateField(label='Дата рождения')
    edu_organisation = forms.ModelChoiceField(label='Место обучения', widget=forms.Select, queryset=edu_organisations,
                                              disabled=True)
    department = forms.CharField(label='Факультет/кафедра', max_length=255)
    speciality = forms.CharField(label='Программа/направление', max_length=255)
    degree = forms.ChoiceField(label='Обучение на квалификацию', choices=DEGREE)
    passport_number = forms.CharField(label='Серия и номер паспорта', max_length=255)
    phone_number = forms.CharField(label='Контактный номер', max_length=255)
    address = forms.CharField(label='Фактический адрес проживания в КР', max_length=255)

    class Meta:
        model = StudentForeign
        fields = ('full_name', 'country', 'ethnical_kyrgyz', 'education_type', 'date_of_birth', 'edu_organisation',
                  'department', 'speciality', 'degree', 'passport_number', 'phone_number', 'address')
