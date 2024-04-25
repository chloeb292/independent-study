from django import forms

from .models import Course, UploadedMaterial, Professor, Assignment, Quiz, Student_Assignment, Student_Quiz
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'course_OASIS_id', 'description', 'semester', 'year']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'course_OASIS_id': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'semester': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class UploadedMaterialForm(forms.ModelForm):
    class Meta:
        model = UploadedMaterial
        fields = ['title', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        
    LANGUAGE_CHOICES = (("python", "Python"), ("java", "Java"), ("c", "C"), ("c++", "C++"), ("other", "Other"))
    DIFFICULTY_CHOICES =(
        ("elementary", "Elementary"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    )

    goal_of_assignment = forms.CharField(widget=forms.Textarea, required=False)

    programming_language = forms.ChoiceField(choices=LANGUAGE_CHOICES, widget=forms.Select, required=False)
    if programming_language == 'other':
        programming_language = forms.CharField(max_length=100, required=False)
    
    difficulty_level = forms.ChoiceField(choices=DIFFICULTY_CHOICES, widget=forms.Select, required=False)
    total_points = forms.IntegerField(min_value=1, max_value=100, required=False)
    specific_requirements_and_instructions = forms.CharField(widget=forms.Textarea, required=False)

    limit_to_selected = forms.BooleanField(required=False, label="Limit quiz to specific materials?")
    selected_materials = forms.ModelMultipleChoiceField(queryset=UploadedMaterial.objects.none(), required=False)

    def __init__(self, *args, **kwargs):
        course = kwargs.pop('course', None)
        super(AssignmentForm, self).__init__(*args, **kwargs)
        if course:
            self.fields['selected_materials'].queryset = UploadedMaterial.objects.filter(course=course)
            print("MATERIALS",self.fields['selected_materials'].queryset)



class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


    LANGUAGE_CHOICES = (("python", "Python"), ("java", "Java"), ("c", "C"), ("c++", "C++"), ("other", "Other"))

    DIFFICULTY_CHOICES =(
        ("elementary", "Elementary"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    )
    Q_STYLE_CHOICES = (
        ("multiple_choice", "Multiple Choice"),
        ("short_answer", "Short Answer"),
    )
    Q_TYPE_CHOICES = (
        ("syntax", "Snippet Syntax Focus"),
        ("logic", "Logic Explanation (no code)"),
        ("output", "Predict Output"),
        ("code", "Write Short Coding Solution"),
        ("complete_code", "Complete Pre-Written Code"),
        ("other", "Other"),

    )
    
    topics_and_concepts = forms.CharField(max_length=200, required=False)
    goal_of_quiz = forms.CharField(widget=forms.Textarea, required=False)
    
    # Select dropdowns
    programming_language = forms.ChoiceField(choices=LANGUAGE_CHOICES, widget=forms.Select, required=False)
    if programming_language == 'other':
        programming_language = forms.CharField(max_length=100, required=False)

    difficulty_level = forms.ChoiceField(choices=DIFFICULTY_CHOICES, widget=forms.Select, required=False)
    num_questions = forms.IntegerField(min_value=1, max_value=50, required=False)
    total_points = forms.IntegerField(min_value=1, max_value=100, required=False)
    fixed_points_per_question = forms.BooleanField(required=False)

    question_type = forms.MultipleChoiceField(choices=Q_TYPE_CHOICES, widget=forms.SelectMultiple, required=False)
    question_style = forms.MultipleChoiceField(choices=Q_STYLE_CHOICES, widget=forms.SelectMultiple, required=False)

    # MATERIAL SELECTION
    limit_to_selected = forms.BooleanField(required=False, label="Limit quiz to specific materials?")
    selected_materials = forms.ModelMultipleChoiceField(queryset=UploadedMaterial.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        course = kwargs.pop('course', None)
        super(QuizForm, self).__init__(*args, **kwargs)
        if course:
            self.fields['selected_materials'].queryset = UploadedMaterial.objects.filter(course=course)
    

class StudentAssignmentAnswerForm(forms.ModelForm):
    class Meta:
        model = Student_Assignment
        fields = ['student_f_name', 'student_l_name', 'submission']
        widgets = {
            'student_f_name': forms.TextInput(attrs={'class': 'form-control'}),
            'student_l_name': forms.TextInput(attrs={'class': 'form-control'}),
            'submission': forms.FileInput(attrs={'class': 'form-control'}),
        }


class StudentQuizAnswerForm(forms.ModelForm):
    class Meta:
        model = Student_Quiz
        fields = ['student_f_name', 'student_l_name', 'submission']
        widgets = {
            'student_f_name': forms.TextInput(attrs={'class': 'form-control'}),
            'student_l_name': forms.TextInput(attrs={'class': 'form-control'}),
            'submission': forms.FileInput(attrs={'class': 'form-control'}),
        }