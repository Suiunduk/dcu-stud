from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from students.models import Student
from universities.models import University
from users.models import CustomUser

universities = University.objects.all()

STATUS = [
    ('Зачислен', 'Зачислен'),
    ('Переведен на следующий курс', 'Переведен на следующий курс'),
    ('Академический отпуск', 'Академический отпуск'),
    ('Отчислен', 'Отчислен')
]

GENDER = [
    ('Мужской', 'Мужской'),
    ('Женский', 'Женский')
]

PREVEDU = [
    ('ВУЗ', 'ВУЗ'),
    ('Другое(школа, колледж и тд.)', 'Другое(школа, колледж и тд.)'),
]

EDU_PROGRAM = [
    ('Бакалавр', 'Бакалавр'),
    ('Магистратура', 'Магистратура'),
    ('Докторантура', 'Докторантура'),
    ('Языковая стажировка', 'Языковая стажировка'),
    ('Летняя школа', 'Летняя школа'),
    ('Стажировка', 'Стажировка'),
    ('Другое', 'Другое')
]

PARENT_TYPE = [
    ('', ''),
    ('Отец', 'Отец'),
    ('Мать', 'Мать'),
    ('Брат/Сестра', 'Брат/Сестра'),
    ('Другой родственник', 'Другой родственник')
]

EDU_FORM = [
    ('Бюджет', 'Бюджет'),
    ('Стипендия', 'Стипендия'),
    ('Контракт', 'Контракт')
]


class StudentSignUpForm(UserCreationForm):
    lastname = forms.CharField(label='Фамилия', max_length=100)
    firstname = forms.CharField(label='Имя', max_length=100)
    fathersname = forms.CharField(label='Отчество', max_length=100, required=False)
    date_of_birth = forms.DateField(label='Дата рождения', widget=forms.SelectDateWidget)
    gender = forms.ChoiceField(label='Пол', choices=GENDER)
    last_edu = forms.ChoiceField(label='Предыдущее образование', choices=PREVEDU)
    university = forms.ModelChoiceField(label='Предыдущий ВУЗ', widget=forms.Select, queryset=universities)
    last_education_place = forms.CharField(label='Предыдущая школа', max_length=100, required=False)
    education_country = forms.CharField(label='Страна обучения', max_length=100)
    university_name = forms.CharField(label='Название зарубежгого учебного заведения', max_length=220)
    year_of_applying = forms.DateField(label='Год поступления', widget=forms.SelectDateWidget)
    education_program = forms.ChoiceField(label='Программа обучения', choices=EDU_PROGRAM)
    education_period = forms.IntegerField(label='Период обучения', max_value=10)
    speciality = forms.CharField(label='Специальность', max_length=220)
    education_form = forms.ChoiceField(label='форма обучения', choices=EDU_FORM)
    status = forms.ChoiceField(label='Статус', choices=STATUS)
    phone_number = forms.CharField(label='Номер телефона', max_length=20)
    email = forms.EmailField(label='Email', )
    parent_name = forms.CharField(label='ФИО одного из родственников', max_length=100)
    parent_type = forms.ChoiceField(label='Степень родства', choices=PARENT_TYPE)
    parent_phone_number = forms.CharField(label='Номер телефона', max_length=100)
    parent_second_name = forms.CharField(label='ФИО ещё одного родственника', max_length=100, required=False)
    parent_second_type = forms.ChoiceField(label='Степень родства', choices=PARENT_TYPE, required=False)
    parent_second_phone_number = forms.CharField(label='Номер телефона', max_length=100, required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'lastname', 'firstname')

    @transaction.atomic
    def save(self):
        user = super(StudentSignUpForm, self).save(commit=False)
        user.is_student = True
        user.username = self.cleaned_data.get('email')
        user.save()
        student = Student.objects.create(user=user,
                                         lastname=self.cleaned_data.get('lastname'),
                                         firstname=self.cleaned_data.get('firstname'),
                                         fathersname=self.cleaned_data.get('fathersname'),
                                         date_of_birth=self.cleaned_data.get('date_of_birth'),
                                         gender=self.cleaned_data.get('gender'),
                                         last_edu=self.cleaned_data.get('last_edu'),
                                         university=self.cleaned_data.get('university'),
                                         last_education_place=self.cleaned_data.get('last_education_place'),
                                         education_country=self.cleaned_data.get('education_country'),
                                         university_name=self.cleaned_data.get('university_name'),
                                         year_of_applying=self.cleaned_data.get('year_of_applying'),
                                         education_program=self.cleaned_data.get('education_program'),
                                         education_period=self.cleaned_data.get('education_period'),
                                         speciality=self.cleaned_data.get('speciality'),
                                         education_form=self.cleaned_data.get('education_form'),
                                         status=self.cleaned_data.get('status'),
                                         phone_number=self.cleaned_data.get('phone_number'),
                                         email=self.cleaned_data.get('email'),
                                         parent_name=self.cleaned_data.get('parent_name'),
                                         parent_type=self.cleaned_data.get('parent_type'),
                                         parent_phone_number=self.cleaned_data.get('parent_phone_number'),
                                         parent_second_name=self.cleaned_data.get('parent_second_name'),
                                         parent_second_type=self.cleaned_data.get('parent_second_type'),
                                         parent_second_phone_number=self.cleaned_data.get('parent_second_phone_number'))
        return user


class StudentCreateForm(UserCreationForm):
    lastname = forms.CharField(label='Фамилия', max_length=100)
    firstname = forms.CharField(label='Имя', max_length=100)
    fathersname = forms.CharField(label='Отчество', max_length=100, required=False)
    date_of_birth = forms.DateField(label='Дата рождения', widget=forms.SelectDateWidget)
    gender = forms.ChoiceField(label='Пол', choices=GENDER)
    last_edu = forms.ChoiceField(label='Предыдущее образование', choices=PREVEDU)
    university = forms.ModelChoiceField(label='Предыдущий ВУЗ', widget=forms.Select, queryset=universities)
    last_education_place = forms.CharField(label='Предыдущая школа', max_length=100, required=False)
    education_country = forms.CharField(label='Страна обучения', max_length=100)
    university_name = forms.CharField(label='Название зарубежгого учебного заведения', max_length=220)
    year_of_applying = forms.DateField(label='Год поступления', widget=forms.SelectDateWidget)
    education_program = forms.ChoiceField(label='Программа обучения', choices=EDU_PROGRAM)
    education_period = forms.IntegerField(label='Период обучения', max_value=10)
    speciality = forms.CharField(label='Специальность', max_length=220)
    education_form = forms.ChoiceField(label='форма обучения', choices=EDU_FORM)
    status = forms.ChoiceField(label='Статус', choices=STATUS)
    phone_number = forms.CharField(label='Номер телефона', max_length=20)
    email = forms.EmailField(label='Email', )
    parent_name = forms.CharField(label='ФИО одного из родственников', max_length=100)
    parent_type = forms.ChoiceField(label='Степень родства', choices=PARENT_TYPE)
    parent_phone_number = forms.CharField(label='Номер телефона', max_length=100)
    parent_second_name = forms.CharField(label='ФИО ещё одного родственника', max_length=100, required=False)
    parent_second_type = forms.ChoiceField(label='Степень родства', choices=PARENT_TYPE, required=False)
    parent_second_phone_number = forms.CharField(label='Номер телефона', max_length=100, required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email',)

    @transaction.atomic
    def save(self):
        user = super(StudentCreateForm, self).save(commit=False)
        user.is_student = True
        user.username = self.cleaned_data.get('email')
        user.save()
        student = Student.objects.create(user=user,
                                         lastname=self.cleaned_data.get('lastname'),
                                         firstname=self.cleaned_data.get('firstname'),
                                         fathersname=self.cleaned_data.get('fathersname'),
                                         date_of_birth=self.cleaned_data.get('date_of_birth'),
                                         gender=self.cleaned_data.get('gender'),
                                         last_edu=self.cleaned_data.get('last_edu'),
                                         university=self.cleaned_data.get('university'),
                                         last_education_place=self.cleaned_data.get('last_education_place'),
                                         education_country=self.cleaned_data.get('education_country'),
                                         university_name=self.cleaned_data.get('university_name'),
                                         year_of_applying=self.cleaned_data.get('year_of_applying'),
                                         education_program=self.cleaned_data.get('education_program'),
                                         education_period=self.cleaned_data.get('education_period'),
                                         speciality=self.cleaned_data.get('speciality'),
                                         education_form=self.cleaned_data.get('education_form'),
                                         status=self.cleaned_data.get('status'),
                                         phone_number=self.cleaned_data.get('phone_number'),
                                         email=self.cleaned_data.get('email'),
                                         parent_name=self.cleaned_data.get('parent_name'),
                                         parent_type=self.cleaned_data.get('parent_type'),
                                         parent_phone_number=self.cleaned_data.get('parent_phone_number'),
                                         parent_second_name=self.cleaned_data.get('parent_second_name'),
                                         parent_second_type=self.cleaned_data.get('parent_second_type'),
                                         parent_second_phone_number=self.cleaned_data.get(
                                             'parent_second_phone_number'))
        return user


class StudentUpdateForm(forms.ModelForm):
    lastname = forms.CharField(label='Фамилия', max_length=100)
    firstname = forms.CharField(label='Имя', max_length=100)
    fathersname = forms.CharField(label='Отчество', max_length=100, required=False)
    date_of_birth = forms.DateField(label='Дата рождения', widget=forms.DateInput)
    gender = forms.ChoiceField(label='Пол', choices=GENDER)
    last_edu = forms.ChoiceField(label='Предыдущее образование', choices=PREVEDU)
    university = forms.ModelChoiceField(label='Предыдущий ВУЗ', widget=forms.Select, queryset=universities)
    last_education_place = forms.CharField(label='Предыдущая школа', max_length=100, required=False)
    education_country = forms.CharField(label='Страна обучения', max_length=100)
    university_name = forms.CharField(label='Название зарубежгого учебного заведения', max_length=220)
    year_of_applying = forms.DateField(label='Год поступления', widget=forms.DateInput)
    education_program = forms.ChoiceField(label='Программа обучения', choices=EDU_PROGRAM)
    education_period = forms.IntegerField(label='Период обучения', max_value=10)
    speciality = forms.CharField(label='Специальность', max_length=220)
    education_form = forms.ChoiceField(label='форма обучения', choices=EDU_FORM)
    status = forms.ChoiceField(label='Статус', choices=STATUS)
    phone_number = forms.CharField(label='Номер телефона', max_length=20)
    parent_name = forms.CharField(label='ФИО одного из родственников', max_length=100)
    parent_type = forms.ChoiceField(label='Степень родства', choices=PARENT_TYPE)
    parent_phone_number = forms.CharField(label='Номер телефона', max_length=100)
    parent_second_name = forms.CharField(label='ФИО ещё одного родственника', max_length=100, required=False)
    parent_second_type = forms.ChoiceField(label='Степень родства', choices=PARENT_TYPE, required=False)
    parent_second_phone_number = forms.CharField(label='Номер телефона', max_length=100, required=False)

    class Meta:
        model = Student
        fields = ('lastname', 'firstname', 'fathersname', 'date_of_birth', 'gender', 'last_edu', 'university',
                  'last_education_place', 'education_country', 'university_name', 'year_of_applying',
                  'education_program', 'education_period', 'speciality', 'education_form', 'status', 'phone_number',
                  'parent_name', 'parent_type', 'parent_phone_number', 'parent_second_name',
                  'parent_second_type', 'parent_second_phone_number',)


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size': '40', 'class': 'form-control'}))
    sender = forms.EmailField(widget=forms.TextInput(attrs={'size': '40', 'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    copy = forms.BooleanField(required=False)
