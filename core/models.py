from django.db import models


# Create your models here.
class ParentType(models.Model):
    type = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.type}'


class Gender(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'


class TypeOfApplying(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'


class Country(models.Model):
    name_ru = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    latitude = models.FloatField(blank=True)
    longitude = models.FloatField(blank=True)

    def __str__(self):
        return f'{self.name_ru}'


class EducationProgram(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'


class EducationForm(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'


class Status(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'

