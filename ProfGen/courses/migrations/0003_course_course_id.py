# Generated by Django 5.0.4 on 2024-04-16 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_professor'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_id',
            field=models.CharField(default='AAA111', max_length=200),
        ),
    ]
