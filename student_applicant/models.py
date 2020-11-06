from django.utils import timezone

from django.db import models
from django.urls import reverse

from core.models import ParentType, Gender, TypeOfApplying, Country, EducationProgram, EducationForm, Status
from edu_organisation.models import EduOrganisation
from university_local.models import University
from users.models import CustomUser


class StudentApplicant(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)

    lastname = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    fathersname = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField()
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    pin_code = models.CharField(max_length=255)
    edu_organisation = models.ForeignKey(EduOrganisation, on_delete=models.CASCADE, null=True)
    other = models.BooleanField(default=False)
    edu_organisation_other = models.CharField(max_length=255, blank=True)
    graduation_date = models.DateField()
    citizenship = models.ForeignKey(Country, on_delete=models.CASCADE)
    foreign_language_level = models.CharField(max_length=255)
    foreign_language_level_document = models.FileField(upload_to='student_applicant/documents/foreign_lang_level')
    average_mark = models.FloatField(max_length=4)
    average_mark_document = models.FileField(upload_to='student_applicant/documents/average_mark')
    family_members = models.CharField(max_length=255)
    family_members_document = models.FileField(upload_to='student_applicant/documents/family_member')
    address = models.CharField(max_length=255)
    phone_number1 = models.CharField(max_length=255)
    phone_number2 = models.CharField(max_length=255, blank=True)

    email = models.CharField(max_length=255, unique=True)
    profile_photo = models.ImageField(blank=True, upload_to='student_applicant/profile_photos/')

    class Meta:
        ordering = ['lastname', 'firstname', 'fathersname']

    def __str__(self):
        return f'{self.lastname} {self.firstname} {self.fathersname} ({self.email})'

    def get_absolute_url(self):
        return reverse('student-applicant-detail', kwargs={'pk': self.pk})

    def delete(self, *args, **kwargs):
        self.profile_photo.delete()
        self.foreign_language_level_document.delete()
        self.average_mark_document.delete()
        self.family_members_document.delete()
        self.user.delete()
        return super(self.__class__, self).delete(*args, **kwargs)


class StudentApplicantParent(models.Model):
    lastname = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    fathersname = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    parent_type = models.ForeignKey(ParentType, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentApplicant, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.lastname} {self.firstname} {self.fathersname}'


class StudentApplicantDocuments(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='student_applicant/additional_documents/')
    student = models.ForeignKey(StudentApplicant, on_delete=models.CASCADE)
    document_file_created_at = models.DateTimeField(auto_now_add=True)
    document_file_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        studentdocument = StudentApplicantDocuments.objects.get(id=self.pk)
        student = studentdocument.student
        return reverse('student-applicant-detail', kwargs={'pk': student.user_id})

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)