# Generated by Django 3.1 on 2020-11-05 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('edu_organisation', '0001_initial'),
        ('student_abroad', '0003_remove_studentabroad_education_period_months'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentabroad',
            name='college',
        ),
        migrations.RemoveField(
            model_name='studentabroad',
            name='school',
        ),
        migrations.RemoveField(
            model_name='studentabroad',
            name='university',
        ),
        migrations.AddField(
            model_name='studentabroad',
            name='edu_organisation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='edu_organisation.eduorganisation'),
        ),
    ]
