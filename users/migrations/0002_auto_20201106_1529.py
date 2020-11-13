# Generated by Django 3.1 on 2020-11-06 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_employee',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_student',
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('student_abroad', 'Студент за рубежом'), ('university_employee', 'Сотрудник университета'), ('student_candidate', 'Кандидат на отбор в конкурсе')], default='student_abroad', max_length=255, verbose_name='Тип пользователя'),
        ),
    ]