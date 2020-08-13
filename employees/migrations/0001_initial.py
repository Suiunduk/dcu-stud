# Generated by Django 3.1 on 2020-08-13 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0003_auto_20200813_1117'),
        ('universities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.customuser')),
                ('lastname', models.CharField(max_length=200, verbose_name='Фамилия')),
                ('firstname', models.CharField(max_length=200, verbose_name='Имя')),
                ('fathersname', models.CharField(blank=True, max_length=200, verbose_name='Отчество')),
                ('phone_number', models.CharField(max_length=200, unique=True, verbose_name='Номер телефона')),
                ('email', models.CharField(max_length=200, unique=True, verbose_name='E-mail')),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='universities.university')),
            ],
            options={
                'ordering': ['lastname', 'firstname', 'fathersname'],
            },
        ),
    ]
