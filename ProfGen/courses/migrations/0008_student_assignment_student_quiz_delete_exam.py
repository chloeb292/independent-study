# Generated by Django 5.0.4 on 2024-04-23 03:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_assignment_answerkey'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student_Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_f_name', models.CharField(max_length=200)),
                ('student_l_name', models.CharField(max_length=200)),
                ('submission', models.TextField()),
                ('grade', models.IntegerField()),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.assignment')),
            ],
        ),
        migrations.CreateModel(
            name='Student_Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_f_name', models.CharField(max_length=200)),
                ('student_l_name', models.CharField(max_length=200)),
                ('submission', models.TextField()),
                ('grade', models.IntegerField()),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.quiz')),
            ],
        ),
        migrations.DeleteModel(
            name='Exam',
        ),
    ]
