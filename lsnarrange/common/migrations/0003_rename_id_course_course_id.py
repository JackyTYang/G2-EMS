# Generated by Django 3.2.4 on 2021-06-24 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20210624_0000'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='id',
            new_name='Course_id',
        ),
    ]
