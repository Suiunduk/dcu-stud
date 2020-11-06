# Generated by Django 3.1 on 2020-11-05 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('announcement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnnouncementDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('file', models.FileField(upload_to='announcements/announcement_documents/')),
                ('document_file_created_at', models.DateTimeField(auto_now_add=True)),
                ('document_file_updated_at', models.DateTimeField(auto_now=True)),
                ('announcement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='announcement.announcement')),
            ],
        ),
    ]
