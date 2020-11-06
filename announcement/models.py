from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

# Create your models here.
from core.models import Country

STATUS_CHOICES = (
    ('active', _("Актуальный конкурс")),
    ('inactive', _("Просроченный конкурс")),
)


class Announcement(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Название программы"))
    description = models.TextField(verbose_name=_("Описание программы"))
    created_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата публикации"))
    beginning_date = models.DateField(verbose_name=_("Дата начала"))
    end_date = models.DateField(verbose_name=_("Дата окончания"))
    destination_country = models.ForeignKey(Country, verbose_name=_("Страна обучения"), on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, default="active", max_length=255,
                              verbose_name=_("Название программы"))

    def get_absolute_url(self):
        return reverse('announcement-detail', kwargs={'pk': self.pk})


class AnnouncementDocument(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='announcements/announcement_documents/')
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    document_file_created_at = models.DateTimeField(auto_now_add=True)
    document_file_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        announcementtdocument = AnnouncementDocument.objects.get(id=self.pk)
        announcement = announcementtdocument.announcement
        return reverse('announcement-detail', kwargs={'pk': announcement.id})

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)
