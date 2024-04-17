from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from courses.models import Course
from courses.forms import AssignmentForm
from decouple import config
from IPython.display import display
from IPython.display import Markdown
import google.generativeai as genai
import os, pathlib, textwrap

GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)


# Create your views here.
@login_required
def create_assignment(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, course=course)
        if form.is_valid():
            data = form.cleaned_data
            content = generate_assignment_content(data)

            assignment = form.save(commit=False)
            assignment.course = course
            assignment.content = content
            assignment.save()
            return redirect('course_detail', course_id=course_id)
    else:
        form = AssignmentForm(course=course)
    return render(request, 'courses/create_assignment.html', {'form': form, 'course': course})

def generate_assignment_content(data):
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])

    user_input = textwrap.dedent(f""" You are a professor creating an assignment for your course. You will generate a coding assignment that is 1-2 questions in length. This assignment is for college students so it should be challenging, and take at least 2-5 hours to complete. To complete the assignment the student must have a deep understanding of the topics that will be specified. You will incorperate the following requirements into this assignment:
    The topics and concepts that the student must understand are: {data['topics_and_concepts']}.
    The goal of this assignment is: {data['goal_of_assignment']}.
    The programming language that the student must use is: {data['programming_language']}.
    The difficulty level of this assignment is: {data['difficulty_level']}.
    The total points for this assignment is: {data['total_points']}. Please distribute the points according to the difficulty of the questions.
    The specific requirements and instructions for this assignment are: {data['specific_requirements_and_instructions']}.                     
    """)
    if data['limit_to_selected'] and data['selected_materials']:
        user_input += "The assignment should be limited to the selected materials. Do not reference anything that is not found in the selected materials."
    
    response = chat.send_message(user_input)

    return response
