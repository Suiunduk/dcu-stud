# Generated by Django 3.1 on 2020-11-12 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='latitude',
            field=models.FloatField(blank=True, verbose_name='Широта'),
        ),
        migrations.AlterField(
            model_name='country',
            name='longitude',
            field=models.FloatField(blank=True, verbose_name='Долгота'),
        ),
        migrations.AlterField(
            model_name='country',
            name='name_en',
            field=models.CharField(max_length=255, verbose_name='Название на английском'),
        ),
        migrations.AlterField(
            model_name='country',
            name='name_ru',
            field=models.CharField(max_length=255, verbose_name='Название на русском'),
        ),
        migrations.AlterField(
            model_name='educationform',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Форма обучения'),
        ),
        migrations.AlterField(
            model_name='educationprogram',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Программа обучения'),
        ),
        migrations.AlterField(
            model_name='gender',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='parenttype',
            name='type',
            field=models.CharField(max_length=255, verbose_name='Степень родства'),
        ),
        migrations.AlterField(
            model_name='status',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Статус студента'),
        ),
        migrations.AlterField(
            model_name='typeofapplying',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Линия поступления'),
        ),
    ]
