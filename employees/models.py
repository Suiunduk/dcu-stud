from django.db import models
from django.urls import reverse

from universities.models import University
from users.models import CustomUser


class Employee(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    lastname = models.CharField('Фамилия', max_length=255)
    firstname = models.CharField('Имя', max_length=255)
    fathersname = models.CharField('Отчество', max_length=255, blank=True)
    phone_number = models.CharField('Номер телефона', max_length=255, unique=True)
    email = models.CharField('E-mail', max_length=255, unique=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE)

    class Meta:
        ordering = ['lastname', 'firstname', 'fathersname']

    def __str__(self):
        return f'{self.lastname} {self.firstname} {self.fathersname} ({self.phone_number})'

    def get_absolute_url(self):
        return reverse('employee-detail', kwargs={'pk': self.pk})

    def delete(self, *args, **kwargs):
        self.user.delete()
        return super(self.__class__, self).delete(*args, **kwargs)
