# Generated by Django 3.1 on 2020-11-09 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcement', '0004_announcementadditionaldocumentnames'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcementapplicants',
            name='rejection_reason',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='announcementapplicants',
            name='status',
            field=models.CharField(choices=[('confirmed', 'Подтвежденный участник'), ('waiting', 'В ожидании подтверждения'), ('not_confirmed', 'Не подтвержденный')], default='not_confirmed', max_length=255, verbose_name='Статус кандидата'),
        ),
    ]
