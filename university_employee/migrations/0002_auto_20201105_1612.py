# Generated by Django 3.1 on 2020-11-05 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('edu_organisation', '0001_initial'),
        ('university_employee', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='university',
        ),
        migrations.AddField(
            model_name='employee',
            name='edu_organisation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='edu_organisation.eduorganisation'),
            preserve_default=False,
        ),
    ]
