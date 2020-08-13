from django.utils import timezone

from django.db import models
from django.urls import reverse

from universities.models import University
from users.models import CustomUser


class Student(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    lastname = models.CharField('Фамилия', max_length=200)
    firstname = models.CharField('Имя', max_length=200)
    fathersname = models.CharField('Отчество', max_length=200, blank=True)
    date_of_birth = models.DateField('Дата рождения')
    gender = models.CharField('Пол', max_length=10, default='Мужской')
    last_edu = models.CharField('Последнее место обучения', max_length=70)
    last_education_place = models.CharField('Название предыдущего учебного заведения', max_length=220, blank=True)
    education_country = models.CharField('Страна обучения', max_length=200)
    university_name = models.CharField('Название учебного заведения', max_length=200)
    year_of_applying = models.DateField('Год поступления', default=timezone.now)
    education_program = models.CharField('Программа обучения', max_length=200)
    education_period = models.CharField('Период обучения', max_length=200)
    speciality = models.CharField('Специальность', max_length=200)
    education_form = models.CharField('Форма обучения', max_length=20, default='Контракт')
    status = models.CharField('Статус студента', max_length=200, default='Зачислен')
    phone_number = models.CharField('Номер телефона', max_length=200, unique=True)
    email = models.CharField('E-mail', max_length=200, unique=True)
    parent_name = models.CharField('ФИО родственника', max_length=200)
    parent_type = models.CharField('Степень родства', max_length=200)
    parent_phone_number = models.CharField('Телефонные номера', max_length=200)
    parent_second_name = models.CharField('ФИО второго родственника', max_length=200, blank=True)
    parent_second_type = models.CharField('Степень родства', max_length=200, blank=True)
    parent_second_phone_number = models.CharField('Телефонные номера', max_length=200, blank=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE)

    class Meta:
        ordering = ['lastname', 'firstname', 'fathersname']

    def __str__(self):
        return f'{self.lastname} {self.firstname} {self.fathersname} ({self.phone_number})'

    #def get_absolute_url(self):
    #    return reverse('student-detail', kwargs={'pk': self.pk})