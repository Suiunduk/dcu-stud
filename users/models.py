from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
