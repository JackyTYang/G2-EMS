# Generated by Django 3.2.4 on 2021-06-23 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='Course_id',
            new_name='id',
        ),
        migrations.AlterField(
            model_name='course',
            name='teacher_id',
            field=models.CharField(max_length=15),
        ),
    ]
