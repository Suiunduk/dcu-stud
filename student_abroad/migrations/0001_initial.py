# Generated by Django 3.1 on 2020-10-28 17:10

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('university_local', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentAbroadCommon',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.customuser')),
                ('lastname', models.CharField(max_length=255)),
                ('firstname', models.CharField(max_length=255)),
                ('fathersname', models.CharField(blank=True, max_length=255)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(default='Мужской', max_length=10)),
                ('last_school', models.CharField(blank=True, max_length=255)),
                ('type_of_applying', models.CharField(default='по линии межвузовских Соглашений', max_length=255)),
                ('education_country', models.CharField(max_length=255)),
                ('university_name', models.CharField(max_length=255)),
                ('year_of_applying', models.DateField(default=django.utils.timezone.now)),
                ('education_program', models.CharField(max_length=255)),
                ('education_period', models.CharField(max_length=255)),
                ('speciality', models.CharField(max_length=255)),
                ('education_form', models.CharField(default='Контракт', max_length=20)),
                ('status', models.CharField(default='Зачислен', max_length=255)),
                ('phone_number', models.CharField(max_length=255, unique=True)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('parent_name', models.CharField(max_length=255)),
                ('parent_type', models.CharField(max_length=255)),
                ('parent_phone_number', models.CharField(max_length=255)),
                ('parent_second_name', models.CharField(max_length=255)),
                ('parent_second_type', models.CharField(max_length=255)),
                ('parent_second_phone_number', models.CharField(max_length=255)),
                ('profile_photo', models.ImageField(blank=True, upload_to='student_abroad/profile_photos/')),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='university_local.university')),
            ],
            options={
                'ordering': ['lastname', 'firstname', 'fathersname'],
            },
        ),
        migrations.CreateModel(
            name='StudentDocuments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('file', models.FileField(upload_to='student_abroad/student_documents/')),
                ('document_file_created_at', models.DateTimeField(auto_now_add=True)),
                ('document_file_updated_at', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_abroad.studentabroad')),
            ],
        ),
    ]
