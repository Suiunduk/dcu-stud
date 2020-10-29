from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms import modelformset_factory
from django.forms.utils import ValidationError

from core.models import Status, Gender, TypeOfApplying, Country, EducationProgram, EducationForm
from student_abroad.models import StudentAbroad, StudentDocuments
from university_local.models import University
from users.models import CustomUser

universities = University.objects.all()
genders = Gender.objects.all()
statuses = Status.objects.all()
types_of_applying = TypeOfApplying.objects.all()
countries = Country.objects.all()
edu_programs = EducationProgram.objects.all()
edu_forms = EducationForm.objects.all()


#
# STATUS = [
#     ('Зачислен', 'Зачислен'),
#     ('Переведен на следующий курс', 'Переведен на следующий курс'),
#     ('Академический отпуск', 'Академический отпуск'),
#     ('Отчислен', 'Отчислен')
# ]
#
# GENDER = [
#     ('Мужской', 'Мужской'),
#     ('Женский', 'Женский')
# ]
#
# EDU_PROGRAM = [
#     ('Бакалавр', 'Бакалавр'),
#     ('Магистратура', 'Магистратура'),
#     ('Докторантура', 'Докторантура'),
#     ('Языковая стажировка', 'Языковая стажировка'),
#     ('Летняя школа', 'Летняя школа'),
#     ('Стажировка', 'Стажировка'),
#     ('Другое', 'Другое')
# ]
#
# PARENT_TYPE = [
#     ('', ''),
#     ('Отец', 'Отец'),
#     ('Мать', 'Мать'),
#     ('Брат/Сестра', 'Брат/Сестра'),
#     ('Другой родственник', 'Другой родственник')
# ]
#
# APPLYING_TYPE = [
#     ('по линии Соглашений Министерства образования и науки Кыргызской республики', 'по линии Соглашений Министерства '
#                                                                                    'образования и науки Кыргызской '
#                                                                                    'республики'),
#     ('по линии межвузовских Соглашений', 'по линии межвузовских Соглашений'),
#     ('в частном порядке (самостоятельно)', 'в частном порядке (самостоятельно)')
# ]
#
# EDU_FORM = [
#     ('Бюджет', 'Бюджет'),
#     ('Стипендия', 'Стипендия'),
#     ('Контракт', 'Контракт')
# ]


class StudentSignUpForm(UserCreationForm):
    lastname = forms.CharField(label='Фамилия', max_length=255)
    firstname = forms.CharField(label='Имя', max_length=255)
    fathersname = forms.CharField(label='Отчество', max_length=255, required=False)
    date_of_birth = forms.DateField(label='Дата рождения', widget=forms.SelectDateWidget)
    gender = forms.ModelChoiceField(label='Пол', widget=forms.Select, queryset=genders)
    university = forms.ModelChoiceField(label='Предыдущий ВУЗ', widget=forms.Select, queryset=universities,
                                        required=False)
    school = forms.CharField(label='Школа', max_length=255, required=False)
    college = forms.CharField(label='Колледж', max_length=255, required=False)
    type_of_applying = forms.ModelChoiceField(label='Линия поступления', widget=forms.Select,
                                              queryset=types_of_applying)
    education_country = forms.ModelChoiceField(label='Страна обучения', widget=forms.Select, queryset=countries)
    university_name = forms.CharField(label='Название зарубежгого учебного заведения', max_length=255)
    year_of_applying = forms.DateField(label='Год поступления', widget=forms.SelectDateWidget)
    education_program = forms.ModelChoiceField(label='Программа обучения', widget=forms.Select, queryset=edu_programs)
    education_period_years = forms.IntegerField(label='Период обучения(годы)', max_value=10)
    education_period_months = forms.IntegerField(label='Период обучения(месяцы)', max_value=10)
    speciality = forms.CharField(label='Специальность', max_length=255)
    education_form = forms.ModelChoiceField(label='Форма обучения', widget=forms.Select, queryset=edu_forms)
    status = forms.ModelChoiceField(label='Статус', widget=forms.Select, queryset=statuses)
    email = forms.EmailField(label='Email', )
    profile_photo = forms.ImageField(label='Фотография профиля', widget=forms.widgets.FileInput(), required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'lastname', 'firstname')

    @transaction.atomic
    def save(self):
        user = super(StudentSignUpForm, self).save(commit=False)
        user.is_student = True
        user.username = self.cleaned_data.get('email')
        user.save()
        student = StudentAbroad.objects.create(user=user,
                                               lastname=self.cleaned_data.get('lastname'),
                                               firstname=self.cleaned_data.get('firstname'),
                                               fathersname=self.cleaned_data.get('fathersname'),
                                               date_of_birth=self.cleaned_data.get('date_of_birth'),
                                               gender=self.cleaned_data.get('gender'),
                                               university=self.cleaned_data.get('university'),
                                               school=self.cleaned_data.get('school'),
                                               college=self.cleaned_data.get('college'),
                                               type_of_applying=self.cleaned_data.get('type_of_applying'),
                                               education_country=self.cleaned_data.get('education_country'),
                                               university_name=self.cleaned_data.get('university_name'),
                                               year_of_applying=self.cleaned_data.get('year_of_applying'),
                                               education_program=self.cleaned_data.get('education_program'),
                                               education_period_years=self.cleaned_data.get('education_period_years'),
                                               education_period_months=self.cleaned_data.get('education_period_months'),
                                               speciality=self.cleaned_data.get('speciality'),
                                               education_form=self.cleaned_data.get('education_form'),
                                               status=self.cleaned_data.get('status'),
                                               email=self.cleaned_data.get('email'),
                                               profile_photo=self.cleaned_data.get('profile_photo'))
        return user


class StudentCreateForm(UserCreationForm):
    lastname = forms.CharField(label='Фамилия', max_length=255)
    firstname = forms.CharField(label='Имя', max_length=255)
    fathersname = forms.CharField(label='Отчество', max_length=255, required=False)
    date_of_birth = forms.DateField(label='Дата рождения', widget=forms.SelectDateWidget)
    gender = forms.ModelChoiceField(label='Пол', widget=forms.Select, queryset=genders)
    university = forms.ModelChoiceField(label='Предыдущий ВУЗ', widget=forms.Select, queryset=universities,
                                        required=False)
    school = forms.CharField(label='Школа', max_length=255, required=False)
    college = forms.CharField(label='Колледж', max_length=255, required=False)
    type_of_applying = forms.ModelChoiceField(label='Линия поступления', widget=forms.Select,
                                              queryset=types_of_applying)
    education_country = forms.ModelChoiceField(label='Страна обучения', widget=forms.Select, queryset=countries)
    university_name = forms.CharField(label='Название зарубежгого учебного заведения', max_length=255)
    year_of_applying = forms.DateField(label='Год поступления', widget=forms.SelectDateWidget)
    education_program = forms.ModelChoiceField(label='Программа обучения', widget=forms.Select, queryset=edu_programs)
    education_period_years = forms.IntegerField(label='Период обучения(годы)', max_value=10)
    education_period_months = forms.IntegerField(label='Период обучения(месяцы)', max_value=10)
    speciality = forms.CharField(label='Специальность', max_length=255)
    education_form = forms.ModelChoiceField(label='Форма обучения', widget=forms.Select, queryset=edu_forms)
    status = forms.ModelChoiceField(label='Статус', widget=forms.Select, queryset=statuses)
    email = forms.EmailField(label='Email', )
    profile_photo = forms.ImageField(label='Фотография профиля', widget=forms.widgets.FileInput(), required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email',)

    @transaction.atomic
    def save(self):
        user = super(StudentCreateForm, self).save(commit=False)
        user.is_student = True
        user.username = self.cleaned_data.get('email')
        user.save()
        student = StudentAbroad.objects.create(user=user,
                                               lastname=self.cleaned_data.get('lastname'),
                                               firstname=self.cleaned_data.get('firstname'),
                                               fathersname=self.cleaned_data.get('fathersname'),
                                               date_of_birth=self.cleaned_data.get('date_of_birth'),
                                               gender=self.cleaned_data.get('gender'),
                                               university=self.cleaned_data.get('university'),
                                               school=self.cleaned_data.get('school'),
                                               college=self.cleaned_data.get('college'),
                                               type_of_applying=self.cleaned_data.get('type_of_applying'),
                                               education_country=self.cleaned_data.get('education_country'),
                                               university_name=self.cleaned_data.get('university_name'),
                                               year_of_applying=self.cleaned_data.get('year_of_applying'),
                                               education_program=self.cleaned_data.get('education_program'),
                                               education_period_years=self.cleaned_data.get('education_period_years'),
                                               education_period_months=self.cleaned_data.get('education_period_months'),
                                               speciality=self.cleaned_data.get('speciality'),
                                               education_form=self.cleaned_data.get('education_form'),
                                               status=self.cleaned_data.get('status'),
                                               email=self.cleaned_data.get('email'),
                                               profile_photo=self.cleaned_data.get('profile_photo'))
        return user


class StudentCreateFormForEmp(UserCreationForm):
    lastname = forms.CharField(label='Фамилия', max_length=255)
    firstname = forms.CharField(label='Имя', max_length=255)
    fathersname = forms.CharField(label='Отчество', max_length=255, required=False)
    date_of_birth = forms.DateField(label='Дата рождения', widget=forms.SelectDateWidget)
    gender = forms.ModelChoiceField(label='Пол', widget=forms.Select, queryset=genders)
    university = forms.HiddenInput()
    school = forms.CharField(label='Школа', max_length=255, required=False)
    college = forms.HiddenInput()
    type_of_applying = forms.ModelChoiceField(label='Линия поступления', widget=forms.Select,
                                              queryset=types_of_applying)
    education_country = forms.ModelChoiceField(label='Страна обучения', widget=forms.Select, queryset=countries)
    university_name = forms.CharField(label='Название зарубежгого учебного заведения', max_length=255)
    year_of_applying = forms.DateField(label='Год поступления', widget=forms.SelectDateWidget)
    education_program = forms.ModelChoiceField(label='Программа обучения', widget=forms.Select, queryset=edu_programs)
    education_period_years = forms.IntegerField(label='Период обучения(годы)', max_value=10)
    education_period_months = forms.IntegerField(label='Период обучения(месяцы)', max_value=10)
    speciality = forms.CharField(label='Специальность', max_length=255)
    education_form = forms.ModelChoiceField(label='Форма обучения', widget=forms.Select, queryset=edu_forms)
    status = forms.ModelChoiceField(label='Статус', widget=forms.Select, queryset=statuses)
    email = forms.EmailField(label='Email', )
    profile_photo = forms.ImageField(label='Фотография профиля', widget=forms.widgets.FileInput(), required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email',)

    @transaction.atomic
    def save(self):
        user = super(StudentCreateFormForEmp, self).save(commit=False)
        user.is_student = True
        user.username = self.cleaned_data.get('email')
        user.save()
        student = StudentAbroad.objects.create(user=user,
                                               lastname=self.cleaned_data.get('lastname'),
                                               firstname=self.cleaned_data.get('firstname'),
                                               fathersname=self.cleaned_data.get('fathersname'),
                                               date_of_birth=self.cleaned_data.get('date_of_birth'),
                                               gender=self.cleaned_data.get('gender'),
                                               university=self.university,
                                               school=self.cleaned_data.get('school'),
                                               college=self.cleaned_data.get('college'),
                                               type_of_applying=self.cleaned_data.get('type_of_applying'),
                                               education_country=self.cleaned_data.get('education_country'),
                                               university_name=self.cleaned_data.get('university_name'),
                                               year_of_applying=self.cleaned_data.get('year_of_applying'),
                                               education_program=self.cleaned_data.get('education_program'),
                                               education_period_years=self.cleaned_data.get('education_period_years'),
                                               education_period_months=self.cleaned_data.get('education_period_months'),
                                               speciality=self.cleaned_data.get('speciality'),
                                               education_form=self.cleaned_data.get('education_form'),
                                               status=self.cleaned_data.get('status'),
                                               email=self.cleaned_data.get('email'),
                                               profile_photo=self.cleaned_data.get('profile_photo'))
        return user


class StudentUpdateForm(forms.ModelForm):
    lastname = forms.CharField(label='Фамилия', max_length=255)
    firstname = forms.CharField(label='Имя', max_length=255)
    fathersname = forms.CharField(label='Отчество', max_length=255, required=False)
    date_of_birth = forms.DateField(label='Дата рождения', widget=forms.SelectDateWidget)
    gender = forms.ModelChoiceField(label='Пол', widget=forms.Select, queryset=genders)
    university = forms.ModelChoiceField(label='Предыдущий ВУЗ', widget=forms.Select, queryset=universities, required=False, disabled=True)
    school = forms.CharField(label='Школа', max_length=255, required=False)
    college = forms.HiddenInput()
    type_of_applying = forms.ModelChoiceField(label='Линия поступления', widget=forms.Select,
                                              queryset=types_of_applying)
    education_country = forms.ModelChoiceField(label='Страна обучения', widget=forms.Select, queryset=countries)
    university_name = forms.CharField(label='Название зарубежгого учебного заведения', max_length=255)
    year_of_applying = forms.DateField(label='Год поступления', widget=forms.SelectDateWidget)
    education_program = forms.ModelChoiceField(label='Программа обучения', widget=forms.Select, queryset=edu_programs)
    education_period_years = forms.IntegerField(label='Период обучения(годы)', max_value=10)
    education_period_months = forms.IntegerField(label='Период обучения(месяцы)', max_value=10)
    speciality = forms.CharField(label='Специальность', max_length=255)
    education_form = forms.ModelChoiceField(label='Форма обучения', widget=forms.Select, queryset=edu_forms)
    status = forms.ModelChoiceField(label='Статус', widget=forms.Select, queryset=statuses)
    profile_photo = forms.ImageField(label='Фотография профиля', widget=forms.widgets.FileInput(), required=False)

    class Meta:
        model = StudentAbroad
        fields = ('lastname', 'firstname', 'fathersname', 'date_of_birth', 'gender', 'university',
                  'school', 'college', 'type_of_applying', 'education_country', 'university_name',
                  'year_of_applying', 'education_program', 'education_period_years', 'education_period_months',
                  'speciality', 'education_form', 'status', 'profile_photo')


class ContactForm(forms.Form):
    full_name = forms.CharField(max_length=100, widget=forms.HiddenInput(attrs={'size': '40', 'class': 'form-control'}),
                                initial='name')
    sender = forms.EmailField(widget=forms.TextInput(attrs={'size': '40', 'class': 'form-control'}))
    subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size': '40', 'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    copy = forms.BooleanField(required=False)


class DocumentUploadForm(forms.ModelForm):
    name = forms.CharField(label='Наименование документа', max_length=255)
    description = forms.CharField(label='Описание', widget=forms.Textarea(attrs={'class': 'form-control'}),
                                  required=False)
    file = forms.FileField(label='Файл', widget=forms.widgets.FileInput())
    student = forms.HiddenInput

    class Meta:
        model = StudentDocuments
        fields = ('name', 'description', 'file',)

    @transaction.atomic
    def save(self):
        student_document = StudentDocuments.objects.create(name=self.cleaned_data.get('name'),
                                                           description=self.cleaned_data.get('description'),
                                                           file=self.cleaned_data.get('file'),
                                                           student=self.student)
