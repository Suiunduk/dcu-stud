from django.db import models
from django.urls import reverse

from university_local.models import University
from users.models import CustomUser


class Employee(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    lastname = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    fathersname = models.CharField(max_length=255, blank=True)
    position = models.CharField(max_length=255, default='Сотрудник')
    phone_number = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
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
