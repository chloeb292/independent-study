# Generated by Django 5.0.4 on 2024-04-17 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_remove_assignment_rubric_alter_uploadedmaterial_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='content',
            field=models.TextField(default='Assignment content will be generated here'),
        ),
    ]