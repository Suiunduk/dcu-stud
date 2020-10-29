from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms import modelformset_factory
from django.forms.utils import ValidationError

from student_abroad.models import StudentAbroad, StudentDocuments
from university_local.models import University
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

APPLYING_TYPE = [
    ('по линии Соглашений Министерства образования и науки Кыргызской республики', 'по линии Соглашений Министерства '
                                                                                   'образования и науки Кыргызской '
                                                                                   'республики'),
    ('по линии межвузовских Соглашений', 'по линии межвузовских Соглашений'),
    ('в частном порядке (самостоятельно)', 'в частном порядке (самостоятельно)')
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
    university = forms.ModelChoiceField(label='Предыдущий ВУЗ', widget=forms.Select, queryset=universities)
    last_school = forms.CharField(label='Предыдущая школа', max_length=100, required=False)
    type_of_applying = forms.ChoiceField(label='Линия поступления', choices=APPLYING_TYPE)
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
    parent_second_name = forms.CharField(label='ФИО ещё одного родственника', max_length=100)
    parent_second_type = forms.ChoiceField(label='Степень родства', choices=PARENT_TYPE)
    parent_second_phone_number = forms.CharField(label='Номер телефона', max_length=100)
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
                                               last_school=self.cleaned_data.get('last_school'),
                                               type_of_applying=self.cleaned_data.get('type_of_applying'),
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
                                               parent_second_phone_number=self.cleaned_data.get('parent_second_phone_number'),
                                               profile_photo=self.cleaned_data.get('profile_photo'))
        return user


class StudentCreateForm(UserCreationForm):
    lastname = forms.CharField(label='Фамилия', max_length=100)
    firstname = forms.CharField(label='Имя', max_length=100)
    fathersname = forms.CharField(label='Отчество', max_length=100, required=False)
    date_of_birth = forms.DateField(label='Дата рождения', widget=forms.SelectDateWidget)
    gender = forms.ChoiceField(label='Пол', choices=GENDER)
    university = forms.ModelChoiceField(label='Предыдущий ВУЗ', widget=forms.Select, queryset=universities)
    last_school = forms.CharField(label='Предыдущая школа', max_length=100, required=False)
    type_of_applying = forms.ChoiceField(label='Линия поступления', choices=APPLYING_TYPE)
    education_country = forms.CharField(label='Страна обучения', max_length=100)
    university_name = forms.CharField(label='Название зарубежгого учебного заведения', max_length=220)
    year_of_applying = forms.DateField(label='Год поступления', widget=forms.SelectDateWidget)
    education_program = forms.ChoiceField(label='Программа обучения', choices=EDU_PROGRAM)
    education_period = forms.IntegerField(label='Период обучения', max_value=10)
    speciality = forms.CharField(label='Специальность', max_length=220)
    education_form = forms.ChoiceField(label='форма обучения', choices=EDU_FORM)
    status = forms.ChoiceField(label='Статус', choices=STATUS)
    phone_number = forms.CharField(label='Номер телефона', max_length=20)
    email = forms.EmailField(label='Email')
    parent_name = forms.CharField(label='ФИО одного из родственников', max_length=100)
    parent_type = forms.ChoiceField(label='Степень родства', choices=PARENT_TYPE)
    parent_phone_number = forms.CharField(label='Номер телефона', max_length=100)
    parent_second_name = forms.CharField(label='ФИО ещё одного родственника', max_length=100)
    parent_second_type = forms.ChoiceField(label='Степень родства', choices=PARENT_TYPE)
    parent_second_phone_number = forms.CharField(label='Номер телефона', max_length=100)
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
                                               last_school=self.cleaned_data.get('last_school'),
                                               type_of_applying=self.cleaned_data.get('type_of_applying'),
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
                                               parent_second_phone_number=self.cleaned_data.get('parent_second_phone_number'),
                                               profile_photo=self.cleaned_data.get('profile_photo'))
        return user


class StudentCreateFormForEmp(UserCreationForm):
    lastname = forms.CharField(label='Фамилия', max_length=100)
    firstname = forms.CharField(label='Имя', max_length=100)
    fathersname = forms.CharField(label='Отчество', max_length=100, required=False)
    date_of_birth = forms.DateField(label='Дата рождения', widget=forms.SelectDateWidget)
    gender = forms.ChoiceField(label='Пол', choices=GENDER)
    university = forms.HiddenInput()
    last_school = forms.CharField(label='Предыдущая школа', max_length=100, required=False)
    type_of_applying = forms.ChoiceField(label='Линия поступления', choices=APPLYING_TYPE)
    education_country = forms.CharField(label='Страна обучения', max_length=100)
    university_name = forms.CharField(label='Название зарубежгого учебного заведения', max_length=220)
    year_of_applying = forms.DateField(label='Год поступления', widget=forms.SelectDateWidget)
    education_program = forms.ChoiceField(label='Программа обучения', choices=EDU_PROGRAM)
    education_period = forms.IntegerField(label='Период обучения', max_value=10)
    speciality = forms.CharField(label='Специальность', max_length=220)
    education_form = forms.ChoiceField(label='форма обучения', choices=EDU_FORM)
    status = forms.ChoiceField(label='Статус', choices=STATUS)
    phone_number = forms.CharField(label='Номер телефона', max_length=20)
    email = forms.EmailField(label='Email')
    parent_name = forms.CharField(label='ФИО одного из родственников', max_length=100)
    parent_type = forms.ChoiceField(label='Степень родства', choices=PARENT_TYPE)
    parent_phone_number = forms.CharField(label='Номер телефона', max_length=100)
    parent_second_name = forms.CharField(label='ФИО ещё одного родственника', max_length=100)
    parent_second_type = forms.ChoiceField(label='Степень родства', choices=PARENT_TYPE)
    parent_second_phone_number = forms.CharField(label='Номер телефона', max_length=100)
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
                                               last_school=self.cleaned_data.get('last_school'),
                                               type_of_applying=self.cleaned_data.get('type_of_applying'),
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
                                               parent_second_phone_number=self.cleaned_data.get('parent_second_phone_number'),
                                               profile_photo=self.cleaned_data.get('profile_photo'))
        return user


class StudentUpdateForm(forms.ModelForm):
    lastname = forms.CharField(label='Фамилия', max_length=100)
    firstname = forms.CharField(label='Имя', max_length=100)
    fathersname = forms.CharField(label='Отчество', max_length=100, required=False)
    date_of_birth = forms.DateField(label='Дата рождения')
    gender = forms.ChoiceField(label='Пол', choices=GENDER)
    university = forms.ModelChoiceField(label='Предыдущий ВУЗ', widget=forms.Select, queryset=universities, disabled=True)
    last_school = forms.CharField(label='Предыдущая школа', max_length=100, required=False)
    type_of_applying = forms.ChoiceField(label='Линия поступления', choices=APPLYING_TYPE)
    education_country = forms.CharField(label='Страна обучения', max_length=100)
    university_name = forms.CharField(label='Название зарубежгого учебного заведения', max_length=220)
    year_of_applying = forms.DateField(label='Год поступления')
    education_program = forms.ChoiceField(label='Программа обучения', choices=EDU_PROGRAM)
    education_period = forms.IntegerField(label='Период обучения', max_value=10)
    speciality = forms.CharField(label='Специальность', max_length=220)
    education_form = forms.ChoiceField(label='форма обучения', choices=EDU_FORM)
    status = forms.ChoiceField(label='Статус', choices=STATUS)
    phone_number = forms.CharField(label='Номер телефона', max_length=20)
    parent_name = forms.CharField(label='ФИО одного из родственников', max_length=100)
    parent_type = forms.ChoiceField(label='Степень родства', choices=PARENT_TYPE)
    parent_phone_number = forms.CharField(label='Номер телефона', max_length=100)
    parent_second_name = forms.CharField(label='ФИО ещё одного родственника', max_length=100)
    parent_second_type = forms.ChoiceField(label='Степень родства', choices=PARENT_TYPE)
    parent_second_phone_number = forms.CharField(label='Номер телефона', max_length=100)

    class Meta:
        model = StudentAbroad
        fields = ('lastname', 'firstname', 'fathersname', 'date_of_birth', 'gender', 'university',
                  'last_school', 'type_of_applying', 'education_country', 'university_name', 'year_of_applying',
                  'education_program', 'education_period', 'speciality', 'education_form', 'status', 'phone_number',
                  'parent_name', 'parent_type', 'parent_phone_number', 'parent_second_name',
                  'parent_second_type', 'parent_second_phone_number', 'profile_photo')


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
