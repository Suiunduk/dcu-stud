import os
import csv
from io import StringIO
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from universities.models import UniversityBulkUpload, University


@receiver(post_save, sender=UniversityBulkUpload)
def create_bulk_university(sender, created, instance, *args, **kwargs):
    if created:
        opened = StringIO(instance.csv_file.read().decode())
        reading = csv.DictReader(opened, delimiter=',')
        universities = []
        for row in reading:
            if 'university_name' in row and row['university_name']:
                name = row['university_name']
                address = row['university_address'] if 'university_address' in row and row['university_address'] else ''

            universities.append(
                University(
                    university_name=name,
                    university_address=address
                )
            )

        University.objects.bulk_create(universities)
        instance.csv_file.close()
        instance.delete()


def _delete_file(path):
    """ Deletes file from filesystem. """
    if os.path.isfile(path):
        os.remove(path)


@receiver(post_delete, sender=UniversityBulkUpload)
def delete_csv_file(sender, instance, *args, **kwargs):
    if instance.csv_file:
        _delete_file(instance.csv_file.path)

