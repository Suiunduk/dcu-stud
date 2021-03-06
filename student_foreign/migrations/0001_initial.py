# Generated by Django 3.1 on 2020-10-29 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('university_local', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentForeign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('ethnical_kyrgyz', models.BooleanField(default=False)),
                ('education_type', models.CharField(default='Очное', max_length=255)),
                ('date_of_birth', models.DateField()),
                ('department', models.CharField(max_length=255)),
                ('speciality', models.CharField(max_length=255)),
                ('degree', models.CharField(max_length=255)),
                ('passport_number', models.CharField(max_length=20)),
                ('phone_number', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='university_local.university')),
            ],
            options={
                'ordering': ['full_name'],
            },
        ),
    ]
