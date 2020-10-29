from django.utils import timezone

from django.db import models
from django.urls import reverse

from core.models import ParentType, Gender, TypeOfApplying, Country, EducationProgram, EducationForm, Status
from university_local.models import University
from users.models import CustomUser


# class StudentCommon(models.Model):

class StudentAbroad(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)

    lastname = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    fathersname = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField()
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)

    university = models.ForeignKey(University, on_delete=models.CASCADE, null=True)
    college = models.CharField(max_length=255, blank=True)
    school = models.CharField(max_length=255, blank=True)

    type_of_applying = models.ForeignKey(TypeOfApplying, on_delete=models.CASCADE)
    education_country = models.ForeignKey(Country, on_delete=models.CASCADE)
    university_name = models.CharField(max_length=255)
    year_of_applying = models.DateField(default=timezone.now)
    education_program = models.ForeignKey(EducationProgram, on_delete=models.CASCADE)
    education_period_years = models.IntegerField()
    education_period_months = models.IntegerField()
    speciality = models.CharField(max_length=255)
    education_form = models.ForeignKey(EducationForm, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    email = models.CharField(max_length=255, unique=True)
    profile_photo = models.ImageField(blank=True, upload_to='student_abroad/profile_photos/')

    class Meta:
        ordering = ['lastname', 'firstname', 'fathersname']

    def __str__(self):
        return f'{self.lastname} {self.firstname} {self.fathersname} ({self.phone_number})'

    def get_absolute_url(self):
        return reverse('student-detail', kwargs={'pk': self.pk})

    def delete(self, *args, **kwargs):
        self.profile_photo.delete()
        self.user.delete()
        return super(self.__class__, self).delete(*args, **kwargs)


class StudentPhoneNumber(models.Model):
    phone_number = models.CharField(max_length=255)
    student = models.ForeignKey(StudentAbroad, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.phone_number)


class StudentParent(models.Model):
    lastname = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    fathersname = models.CharField(max_length=255, blank=True)
    parent_type = models.ForeignKey(StudentAbroad, on_delete=models.CASCADE)
    student = models.ForeignKey(ParentType, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.lastname} {self.firstname} {self.fathersname} ({self.phone_number})'


class StudentParentPhoneNumber(models.Model):
    phone_number = models.CharField(max_length=255)
    parent = models.ForeignKey(StudentParent, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.phone_number)


class StudentDocuments(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='student_abroad/student_documents/')
    student = models.ForeignKey(StudentAbroad, on_delete=models.CASCADE)
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
