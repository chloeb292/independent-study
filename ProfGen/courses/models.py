from django.db import models
from django.contrib.auth.models import User


class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)

    def __str__(self):
        return "Dr." + self.last_name

class Course(models.Model):
    professor = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    course_OASIS_id = models.CharField(max_length=200, default="AAA111")
    description = models.TextField()
    semester = models.CharField(max_length=200)
    year = models.IntegerField()

    def __str__(self):
        return str(self.title)

class UploadedMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='templates/courses/materials/')

    def __str__(self):
        return str(self.title)
    
class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField(default="Assignment content will be generated here")
    answerkey = models.TextField(default="Answer key will be generated here")

    def __str__(self):
        return str(self.title)

class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    questions = models.TextField()
    answerkey = models.TextField()

    def __str__(self):
        return str(self.title)
    
