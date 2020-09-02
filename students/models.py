from django.utils import timezone

from django.db import models
from django.urls import reverse

from universities.models import University
from users.models import CustomUser


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    lastname = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    fathersname = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, default='Мужской')
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    last_school = models.CharField(max_length=255, blank=True)
    education_country = models.CharField(max_length=255)
    university_name = models.CharField(max_length=255)
    year_of_applying = models.DateField(default=timezone.now)
    education_program = models.CharField(max_length=255)
    education_period = models.CharField(max_length=255)
    speciality = models.CharField(max_length=255)
    education_form = models.CharField(max_length=20, default='Контракт')
    status = models.CharField(max_length=255, default='Зачислен')
    phone_number = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    parent_name = models.CharField(max_length=255)
    parent_type = models.CharField(max_length=255)
    parent_phone_number = models.CharField(max_length=255)
    parent_second_name = models.CharField(max_length=255)
    parent_second_type = models.CharField(max_length=255)
    parent_second_phone_number = models.CharField(max_length=255)
    profile_photo = models.ImageField(blank=True, upload_to='students/profile_photos/')

    class Meta:
        ordering = ['lastname', 'firstname', 'fathersname']

    def __str__(self):
        return f'{self.lastname} {self.firstname} {self.fathersname} ({self.phone_number})'

    def get_absolute_url(self):
        return reverse('student-detail', kwargs={'pk': self.pk})

    def delete(self, *args, **kwargs):
        self.user.delete()
        return super(self.__class__, self).delete(*args, **kwargs)


class StudentDocuments(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='students/student_documents/')
    student = models.ForeignKey(Student, on_delete=models.CheckConstraint)
    document_file_created_at = models.DateTimeField(auto_now_add=True)
    document_file_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        studentdocument = StudentDocuments.objects.get(id=self.pk)
        student = studentdocument.student
        return reverse('student-detail', kwargs={'pk': student.user_id})

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)
