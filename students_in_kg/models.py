from django.db import models
from django.urls import reverse

from universities.models import University


class Student_abroad(models.Model):
    full_name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    ethnical_kyrgyz = models.BooleanField(default=False)
    education_type = models.CharField(max_length=255, default="Очное")
    date_of_birth = models.DateField()
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    department = models.CharField(max_length=255)
    speciality = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    passport_number = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return f'{self.full_name}'

    def get_absolute_url(self):
        return reverse('student-abroad-detail', kwargs={'pk': self.pk})
