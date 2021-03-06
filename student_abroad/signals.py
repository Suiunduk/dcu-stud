import os

from django.db.models.signals import post_delete
from django.dispatch import receiver

from student_abroad.models import StudentAbroad


def _delete_file(path):
    """ Deletes file from filesystem. """
    if os.path.isfile(path):
        os.remove(path)


@receiver(post_delete, sender=StudentAbroad)
def delete_profile_photo_on_delete(sender, instance, *args, **kwargs):
    if instance.profile_photo:
        _delete_file(instance.profile_photo.path)