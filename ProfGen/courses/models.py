from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    professor = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    semester = models.CharField(max_length=200)
    year = models.IntegerField()

    def __str__(self):
        return self.title

class UploadedMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    rubric = models.TextField()

    def __str__(self):
        return self.title

class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    questions = models.TextField()
    answerkey = models.TextField()

    def __str__(self):
        return self.title
    
class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    questions = models.TextField()
    answerkey = models.TextField()


    def __str__(self):
        return self.title