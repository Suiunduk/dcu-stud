from django.db import models

from universities.models import University
from users.models import CustomUser


class Employee(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    lastname = models.CharField('Фамилия', max_length=200)
    firstname = models.CharField('Имя', max_length=200)
    fathersname = models.CharField('Отчество', max_length=200, blank=True)
    phone_number = models.CharField('Номер телефона', max_length=200, unique=True)
    email = models.CharField('E-mail', max_length=200, unique=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE)

    class Meta:
        ordering = ['lastname', 'firstname', 'fathersname']

    def __str__(self):
        return f'{self.lastname} {self.firstname} {self.fathersname} ({self.phone_number})'

    # def get_absolute_url(self):
    #    return reverse('student-detail', kwargs={'pk': self.pk})
