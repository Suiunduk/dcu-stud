from django.db import models

from django.urls import reverse
from django.utils import timezone


class University(models.Model):
    university_name = models.CharField('Название учебного заведения', max_length=255)
    university_address = models.CharField('Фактический адрес учебного заведения', max_length=255)

    def __str__(self):
        return f'{self.university_name}'

    def get_absolute_url(self):
        return reverse('university-detail', kwargs={'pk': self.pk})


class UniversityBulkUpload(models.Model):
    date_uploaded = models.DateTimeField(auto_now=True)
    csv_file = models.FileField(upload_to='students/bulkupload/')
