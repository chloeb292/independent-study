# Generated by Django 5.0.4 on 2024-04-21 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_assignment_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='answerkey',
            field=models.TextField(default='Answer key will be generated here'),
        ),
    ]