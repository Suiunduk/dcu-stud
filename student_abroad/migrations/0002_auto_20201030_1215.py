# Generated by Django 3.1 on 2020-10-30 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('student_abroad', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentparent',
            name='phone_number',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='studentparent',
            name='parent_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.parenttype'),
        ),
        migrations.AlterField(
            model_name='studentparent',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_abroad.studentabroad'),
        ),
        migrations.DeleteModel(
            name='StudentParentPhoneNumber',
        ),
    ]
