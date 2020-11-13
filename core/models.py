from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _


# Create your models here.
class ParentType(models.Model):
    type = models.CharField(verbose_name=_("Степень родства"), max_length=255)

    def __str__(self):
        return f'{self.type}'

    def get_absolute_url(self):
        return reverse('parent-types-list')


class Gender(models.Model):
    name = models.CharField(verbose_name=_("Пол"), max_length=255)

    def __str__(self):
        return f'{self.name}'
    def get_absolute_url(self):
        return reverse('genders-list')


class TypeOfApplying(models.Model):
    name = models.CharField(verbose_name=_("Линия поступления"), max_length=255)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('types-of-applying-list')


class Country(models.Model):
    name_ru = models.CharField(verbose_name=_("Название на русском"), max_length=255)
    name_en = models.CharField(verbose_name=_("Название на английском"), max_length=255)
    longitude = models.DecimalField(verbose_name=_("Долгота"), blank=True, max_digits=9, decimal_places=6)
    latitude = models.DecimalField(verbose_name=_("Широта"), blank=True, max_digits=9, decimal_places=6)

    def __str__(self):
        return f'{self.name_ru}'

    def get_absolute_url(self):
        return reverse('countries-list')


class EducationProgram(models.Model):
    name = models.CharField(verbose_name=_("Программа обучения"), max_length=255)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('education-programs-list')


class EducationForm(models.Model):
    name = models.CharField(verbose_name=_("Форма обучения"), max_length=255)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('education-forms-list')


class Status(models.Model):
    name = models.CharField(verbose_name=_("Статус студента"), max_length=255)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('statuses-list')
