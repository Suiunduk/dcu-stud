from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from announcement.models import AnnouncementApplicants, Announcement
from core.models import Gender, Country, ParentType
from edu_organisation.models import EduOrganisation
from student_applicant.models import StudentApplicant, StudentApplicantParent, StudentApplicantDocuments
from users.models import CustomUser

edu_organisations = EduOrganisation.objects.all()
genders = Gender.objects.all()
countries = Country.objects.all()
parent_types = ParentType.objects.all()


class StudentApplicantSignUpForm(UserCreationForm):
    lastname = forms.CharField(label='Фамилия', max_length=255)
    firstname = forms.CharField(label='Имя', max_length=255)

    email = forms.EmailField(label='Email', )

    announcement = forms.HiddenInput

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

        announcement_applicant = AnnouncementApplicants.objects.create(announcement=self.announcement,
                                                                       applicant=user,
                                                                       status='not_confirmed')

        return user


class StudentApplicantCreateForm(forms.ModelForm):
    lastname = forms.CharField(label='Фамилия', max_length=255, disabled=True, required=False)
    firstname = forms.CharField(label='Имя', max_length=255, disabled=True, required=False)
    fathersname = forms.CharField(label='Отчество', max_length=255, required=False)
    date_of_birth = forms.DateField(label='Дата рождения')
    gender = forms.ModelChoiceField(label='Пол', widget=forms.Select, queryset=genders)
    pin_code = forms.CharField(label='ИНН', max_length=255)
    edu_organisation = forms.ModelChoiceField(label='Предыдущее образование', widget=forms.Select,
                                              queryset=edu_organisations, required=False)
    other = forms.BooleanField(label='Другое место обучения', required=False)
    edu_organisation_other = forms.CharField(label='Пожалуйста укажите другое место обучения', max_length=255,
                                             required=False)
    graduation_date = forms.DateField(label='Дата окончания обучения')
    citizenship = forms.ModelChoiceField(label='Гражданство', widget=forms.Select, queryset=countries)
    foreign_language_level = forms.CharField(label='Знание иностранного языка', max_length=255)
    foreign_language_level_document = forms.FileField(label='Файл подтверждающий знание иностранного языка')
    average_mark = forms.FloatField(label='Средний балл успеваемости')
    average_mark_document = forms.FileField(label='Файл подтверждающий средний балл')
    family_members = forms.CharField(label='Состав семьи', max_length=255)
    family_members_document = forms.FileField(label='Документ подтверждающий состав семьи')
    address = forms.CharField(label='Фактический адрес проживания', max_length=255)
    phone_number1 = forms.CharField(label='Телефонный номер', max_length=255)
    phone_number2 = forms.CharField(label='Дополнительный телефонный номер(если имеется)', max_length=255,
                                    required=False)

    email = forms.CharField(label='Email', max_length=255, disabled=True, required=False)
    profile_photo = forms.ImageField(label='Фотография профиля', required=False)

    parent1_lastname = forms.CharField(label='Фамилия родственника', max_length=255)
    parent1_firstname = forms.CharField(label='Имя родственника', max_length=255)
    parent1_fathersname = forms.CharField(label='Отчество родственника', max_length=255, required=False)
    parent1_address = forms.CharField(label='Адрес родственника', max_length=255)
    parent1_phone_number = forms.CharField(label='Телефонные номера родственника', max_length=255)
    parent1_parent_type = forms.ModelChoiceField(label='Степень родства', widget=forms.Select, queryset=parent_types)

    parent2_lastname = forms.CharField(label='Фамилия второго родственника', max_length=255)
    parent2_firstname = forms.CharField(label='Имя второго родственника', max_length=255)
    parent2_fathersname = forms.CharField(label='Отчество второго родственника', max_length=255, required=False)
    parent2_address = forms.CharField(label='Адрес второго родственника', max_length=255)
    parent2_phone_number = forms.CharField(label='Телефонные номера второго родственника', max_length=255)
    parent2_parent_type = forms.ModelChoiceField(label='Степень родства', widget=forms.Select, queryset=parent_types)


    class Meta:
        model = StudentApplicant

        fields = ('lastname', 'firstname', 'fathersname', 'date_of_birth', 'date_of_birth', 'gender',
                  'pin_code', 'edu_organisation', 'other', 'edu_organisation_other', 'graduation_date', 'citizenship',
                  'foreign_language_level', 'foreign_language_level_document', 'average_mark', 'average_mark_document',
                  'family_members', 'family_members_document', 'address', 'phone_number1', 'phone_number2', 'email',
                  'profile_photo')

    @transaction.atomic
    def save(self):
        student = StudentApplicant.objects.create(user=self.user,
                                                  lastname=self.lastname,
                                                  firstname=self.firstname,
                                                  fathersname=self.cleaned_data.get('fathersname'),
                                                  date_of_birth=self.cleaned_data.get('date_of_birth'),
                                                  gender=self.cleaned_data.get('gender'),
                                                  pin_code=self.cleaned_data.get('pin_code'),
                                                  edu_organisation=self.cleaned_data.get('edu_organisation'),
                                                  other=self.cleaned_data.get('other'),
                                                  edu_organisation_other=self.cleaned_data.get('edu_organisation_other'),
                                                  graduation_date=self.cleaned_data.get('graduation_date'),
                                                  citizenship=self.cleaned_data.get('citizenship'),
                                                  foreign_language_level=self.cleaned_data.get('foreign_language_level'),
                                                  foreign_language_level_document=self.cleaned_data.get('foreign_language_level_document'),
                                                  average_mark=self.cleaned_data.get('average_mark'),
                                                  average_mark_document=self.cleaned_data.get('average_mark_document'),
                                                  family_members=self.cleaned_data.get('family_members'),
                                                  family_members_document=self.cleaned_data.get('family_members_document'),
                                                  address=self.cleaned_data.get('address'),
                                                  phone_number1=self.cleaned_data.get('phone_number1'),
                                                  phone_number2=self.cleaned_data.get('phone_number2'),
                                                  email=self.email,
                                                  profile_photo=self.cleaned_data.get('profile_photo'))

        parent1 = StudentApplicantParent.objects.create(lastname=self.cleaned_data.get('parent1_lastname'),
                                                        firstname=self.cleaned_data.get('parent1_firstname'),
                                                        fathersname=self.cleaned_data.get('parent1_fathersname'),
                                                        address=self.cleaned_data.get('parent1_address'),
                                                        phone_number=self.cleaned_data.get('parent1_phone_number'),
                                                        parent_type=self.cleaned_data.get('parent1_parent_type'),
                                                        student=student)

        parent2 = StudentApplicantParent.objects.create(lastname=self.cleaned_data.get('parent2_lastname'),
                                                        firstname=self.cleaned_data.get('parent2_firstname'),
                                                        fathersname=self.cleaned_data.get('parent2_fathersname'),
                                                        address=self.cleaned_data.get('parent2_address'),
                                                        phone_number=self.cleaned_data.get('parent2_phone_number'),
                                                        parent_type=self.cleaned_data.get('parent2_parent_type'),
                                                        student=student)

        return student


class StudentApplicantUpdateForm(forms.ModelForm):
    lastname = forms.CharField(label='Фамилия', max_length=255, disabled=True, required=False)
    firstname = forms.CharField(label='Имя', max_length=255, disabled=True, required=False)
    fathersname = forms.CharField(label='Отчество', max_length=255, required=False)
    date_of_birth = forms.DateField(label='Дата рождения')
    gender = forms.ModelChoiceField(label='Пол', widget=forms.Select, queryset=genders)
    pin_code = forms.CharField(label='ИНН', max_length=255)
    edu_organisation = forms.ModelChoiceField(label='Предыдущее образование', widget=forms.Select,
                                              queryset=edu_organisations, required=False)
    other = forms.BooleanField(label='Другое место обучения', required=False)
    edu_organisation_other = forms.CharField(label='Пожалуйста укажите другое место обучения', max_length=255,
                                             required=False)
    graduation_date = forms.DateField(label='Дата окончания обучения')
    citizenship = forms.ModelChoiceField(label='Гражданство', widget=forms.Select, queryset=countries)
    foreign_language_level = forms.CharField(label='Знание иностранного языка', max_length=255)
    foreign_language_level_document = forms.FileField(label='Файл подтверждающий знание иностранного языка')
    average_mark = forms.FloatField(label='Средний балл успеваемости')
    average_mark_document = forms.FileField(label='Файл подтверждающий средний балл')
    family_members = forms.CharField(label='Состав семьи', max_length=255)
    family_members_document = forms.FileField(label='Документ подтверждающий состав семьи')
    address = forms.CharField(label='Фактический адрес проживания', max_length=255)
    phone_number1 = forms.CharField(label='Телефонный номер', max_length=255)
    phone_number2 = forms.CharField(label='Дополнительный телефонный номер(если имеется)', max_length=255,
                                    required=False)

    email = forms.CharField(label='Email', max_length=255, disabled=True, required=False)
    profile_photo = forms.ImageField(label='Фотография профиля', required=False)

    class Meta:
        model = StudentApplicant

        fields = ('lastname', 'firstname', 'fathersname', 'date_of_birth', 'date_of_birth', 'gender',
                  'pin_code', 'edu_organisation', 'other', 'edu_organisation_other', 'graduation_date', 'citizenship',
                  'foreign_language_level', 'foreign_language_level_document', 'average_mark', 'average_mark_document',
                  'family_members', 'family_members_document', 'address', 'phone_number1', 'phone_number2', 'email',
                  'profile_photo')


class ApplicantDocumentUploadForm(forms.ModelForm):
    name = forms.CharField(label='Наименование документа', max_length=255)
    description = forms.CharField(label='Описание', widget=forms.Textarea(attrs={'class': 'form-control'}),
                                  required=False)
    file = forms.FileField(label='Файл', widget=forms.widgets.FileInput())
    student = forms.HiddenInput

    class Meta:
        model = StudentApplicantDocuments
        fields = ('name', 'description', 'file',)

    @transaction.atomic
    def save(self):
        student_document = StudentApplicantDocuments.objects.create(name=self.cleaned_data.get('name'),
                                                           description=self.cleaned_data.get('description'),
                                                           file=self.cleaned_data.get('file'),
                                                           student=self.student)
