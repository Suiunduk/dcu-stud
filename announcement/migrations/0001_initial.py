# Generated by Django 3.1 on 2020-11-05 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название программы')),
                ('description', models.TextField(verbose_name='Описание программы')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Дата публикации')),
                ('beginning_date', models.DateField(verbose_name='Дата начала')),
                ('end_date', models.DateField(verbose_name='Дата окончания')),
                ('status', models.CharField(choices=[('active', 'Актуальный конкурс'), ('inactive', 'Просроченный конкурс')], default='active', max_length=255, verbose_name='Название программы')),
                ('destination_country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.country', verbose_name='Страна обучения')),
            ],
        ),
    ]
