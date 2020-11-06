from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

USER_TYPE_CHOICES = (
    ('student_abroad', _("Студент за рубежом")),
    ('university_employee', _("Сотрудник университета")),
    ('student_candidate', _("Кандидат на отбор в конкурсе")),
)


class CustomUser(AbstractUser):
    user_type = models.CharField(choices=USER_TYPE_CHOICES, default="super_user", max_length=255,
                                 verbose_name=_("Тип пользователя"))

