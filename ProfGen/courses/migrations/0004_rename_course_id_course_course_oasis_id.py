# Generated by Django 5.0.4 on 2024-04-16 23:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_course_course_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='course_id',
            new_name='course_OASIS_id',
        ),
    ]
