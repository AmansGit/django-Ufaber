# Generated by Django 2.2 on 2020-08-09 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userlog',
            old_name='project_name',
            new_name='project_id',
        ),
    ]