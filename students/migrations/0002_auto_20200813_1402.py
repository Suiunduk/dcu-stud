# Generated by Django 3.1 on 2020-08-13 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('universities', '0001_initial'),
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='last_university',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='universities.university'),
        ),
    ]