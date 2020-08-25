# Generated by Django 3.1 on 2020-08-24 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('universities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='university',
            name='university_address',
            field=models.CharField(max_length=255, verbose_name='Фактический адрес учебного заведения'),
        ),
        migrations.AlterField(
            model_name='university',
            name='university_name',
            field=models.CharField(max_length=255, verbose_name='Название учебного заведения'),
        ),
    ]
