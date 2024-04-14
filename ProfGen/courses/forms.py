from django import forms

from .models import Course, UploadedMaterial

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'semester', 'year']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'semester': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class AssignmentForm(forms.ModelForm):
    LANGUAGE_CHOICES = (("python", "Python"), ("java", "Java"), ("c", "C"), ("c++", "C++"), ("other", "Other"))
    DIFFICULTY_CHOICES =(
        ("elementary", "Elementary"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    )

    topics_and_concepts = forms.CharField(max_length=200, required=False)
    programming_language = forms.ChoiceField(choices=LANGUAGE_CHOICES, widget=forms.Select, required=False)
    if programming_language == 'other':
        programming_language = forms.CharField(max_length=100, required=False)
    
    difficulty_level = forms.ChoiceField(choices=DIFFICULTY_CHOICES, widget=forms.Select, required=False)
    total_points = forms.IntegerField(min_value=1, max_value=100, required=False)
    specific_requirements_and_instructions = forms.CharField(widget=forms.Textarea, required=False)

    limit_to_selected = forms.BooleanField(required=False, label="Limit quiz to specific materials?")
    selected_materials = forms.ModelMultipleChoiceField(queryset=UploadedMaterial.objects.all(), required=False)



class QuizForm(forms.Form):
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
    
