from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

ORG_TYPE_CHOICES = (
    ('school', _("Школа")),
    ('college', _("СПУЗ")),
    ('lyceum', _("Проф. лицей")),
    ('university', _("ВУЗ")),
)


# Create your models here.
class EduOrganisation(models.Model):
    org_name = models.CharField(max_length=255, verbose_name=_("Наименование учреждения"))
    org_code = models.CharField(max_length=255, verbose_name=_("Код учреждения"), blank=True)
    org_address = models.CharField(max_length=255, verbose_name=_("Адрес учреждения"), blank=True)
    org_type = models.CharField(choices=ORG_TYPE_CHOICES, max_length=255, verbose_name=_("Тип учреждения"))

    def get_absolute_url(self):
        return reverse('organisation-detail', kwargs={'pk': self.pk})
