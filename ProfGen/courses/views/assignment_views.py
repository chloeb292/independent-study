from django.shortcuts import render
import pdfplumber
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from courses.models import Course, Assignment, Student_Assignment
from courses.forms import AssignmentForm, StudentAssignmentAnswerForm
import google.generativeai as genai
import os, pathlib, textwrap
import markdown
from dotenv import load_dotenv
import pytesseract
from PIL import Image
import anthropic

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.getenv('ANTHROPIC_API_KEY'),
)

def generate_response(prompt):
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text

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

def assignment_detail(request, course_id, assignment_id):
    course = get_object_or_404(Course, pk=course_id)
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    graded_assignments = Student_Assignment.objects.filter(assignment=assignment)
    # print("ANSWER KEY", assignment.answerkey)
    return render(request, 'courses/assignment_detail.html', {'course': course, 'assignment': assignment, 'answerkey': assignment.answerkey, 'graded_assignments': graded_assignments})

def delete_assignment(course_id, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    assignment.delete()
    return redirect('course_detail', course_id=course_id)

def generate_assignment_content(data):

    user_input = textwrap.dedent(f""" You are a professor creating an assignment for your course. You will generate a coding assignment that is 1-2 questions in length. This assignment is for college students so it should be challenging, and take at least 2-5 hours to complete. To complete the assignment the student must have a deep understanding of the topics that will be specified. You will incorperate the following requirements into this assignment:
    The title of the assignment is: {data['title']}.
    The description of the assignment is: {data['description']}.
    The goal of this assignment is: {data['goal_of_assignment']}.
    The programming language that the student must use is: {data['programming_language']}.
    The difficulty level of this assignment is: {data['difficulty_level']}.
    The total points for this assignment is: {data['total_points']}. Please distribute the points according to the difficulty of the questions.
    The specific requirements and instructions for this assignment are: {data['specific_requirements_and_instructions']}.                     
    """)
    if data['selected_materials']:

        user_input += "The quiz should be limited to the selected materials. Do not reference anything that is not found in the selected materials."
        for material in data['selected_materials']:
            user_input += f"Material: {material.title}\n{material.text}\n"


    user_input+="""

    Assignment Template:
    ### Assignment Title: [Title Here]

    **Points: [XX pts]**

    **Naming rule:** Name this file `[filename].py`.

    #### Objective:
    Describe the primary goal and application of this assignment.

    #### Task Details:
    1. **Functionality:** What should the program do? List out the functions and their purposes.
    2. **Input/Output:** Specify the input methods (files, user input) and expected output formats.
    3. **Formulas/Methods:** Detail any specific algorithms, formulas, or methods that need to be implemented.

    #### Requirements:
    - **Validation:** Steps for validating inputs or data.
    - **Error Handling:** How should the program respond to incorrect inputs or errors?
    - **External Libraries:** List any required libraries or modules and their usage in the program.

    #### Sample Output/Interaction:
    Provide a clear example of the expected output or a walkthrough of a sample interaction with the program.

    ### Submission Instructions:
    Detail any specific instructions regarding how and where to submit the assignment.

    ---

    IMPORTANT: ASSIGNMENT MUST INCLUDE EACH OF THE ABOVE ELEMENTS TO ENSURE COMPLETENESS AND CLARITY. DO NOT DEVIATE FROM THE SPECIFIED FORMAT. DO NOT CREATE AN ANSWER KEY FOR THIS ASSIGNMENT. When writing comments in the code, do not use '#', simply write the comment or explanation.

    """

    response = generate_response(user_input)

    return response


def generate_answer_key(request, course_id, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)

    user_input = textwrap.dedent(f""" You are a professor creating an answer key for a coding assignment given to your students. Please create an answer key for the following assignment.
    You will need to answer the following assignment as if you were a student. Give full and complete answers, it will likely consist of writing code in Python, C or C++. Write working code that will solve the problem presented in the content.
    
    The assignment is as follows:
    {assignment.content}.

    The format of the answer key should be EXACTLY as follows:
    <code>
    The answer will be a giant block of code that will solve the problem presented in the assignment. Leave all the code here.
    Put comments where necessary to explain the code and how it meets the requirements of the rubric.
    </code>

    IMPORTANT: When writing comments in the code, do not use '#', simply write the comment or explanation.

    At the end of each question, you should have a comment that explains the code and how it meets the requirements of the rubric. This will help the student understand how the code solves the problem and why it is correct.
    
    """)
    
    
    response = generate_response(user_input)
    assignment.answerkey = response
    assignment.save()

    return redirect('assignment_detail', course_id=course_id, assignment_id=assignment_id)
    

def extract_text_from_pdf(file):
    # extract text from a PDF file using pdfplumber and an in-memory file
    with pdfplumber.open(file) as pdf:
        text = " ".join(page.extract_text() for page in pdf.pages)
    return text

def extract_text_from_image(file):
    # Convert the file to an image object
    image = Image.open(file)
    text = pytesseract.image_to_string(image)
    
    return text

def extract_text_from_python(file):
    text = file.read().decode('utf-8')
    return text


def grade_student_assignment(request, course_id, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    if request.method == 'POST':
        form = StudentAssignmentAnswerForm(request.POST, request.FILES)
    else:
        form = StudentAssignmentAnswerForm()

    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        student_f_name = data['student_f_name']
        student_l_name = data['student_l_name']
        uploaded_files = request.FILES.getlist("submission")
        submission_text = ""

        for file in uploaded_files:
            #if image extract text from image (ends with png, jpg, jpeg)
            if file.name.endswith('.png') or file.name.endswith('.jpg') or file.name.endswith('.jpeg'):
                submission_text += extract_text_from_image(file)
            #if pdf extract text from pdf
            elif file.name.endswith('.pdf'):
                submission_text += extract_text_from_pdf(file)
            elif file.name.endswith('.py'):
                submission_text += extract_text_from_python(file)
            else:
                form.add_error(None, "Please upload only PDF files.")
                return render(request, 'courses/grade_student_assignment.html', {'assignment': assignment, 'form': form})

        print("SUBMISSION TEXT", submission_text)   

        # Grade the assignment, compare submission to assignment.content and assignment.answerkey (if assigbment.answerkey exists, if not, generate one)
        if not assignment.answerkey:
            generate_answer_key(request, course_id, assignment_id)

        user_prompt = textwrap.dedent(f""" You are a professor grading a student's assignment. Please grade the following assignment according to the context of the assignment and the answer key provided.
        The student's submission is as follows:
            {submission_text}

        The assignment content is as follows:
            {assignment.content}

        The answer key is as follows:
            {assignment.answerkey}
        
        Please provide a grade for each question in the assignment. Explain why the student received the grade they did. If the student's answer is incorrect, provide feedback on how they can improve.
        """)

        response = generate_response(user_input)

        # Save the student's assignment and grade
        student_assignment = Student_Assignment(student_f_name=student_f_name, student_l_name=student_l_name, assignment=assignment, submission=submission_text, grade=response)
        student_assignment.save()

        return redirect('student_assignment_detail', course_id=course_id, assignment_id=assignment_id, student_assignment_id=student_assignment.id)
    return render(request, 'courses/grade_student_assignment.html', {'assignment': assignment, 'form': form})

def student_assignment_detail(request, course_id, assignment_id, student_assignment_id):
    course = get_object_or_404(Course, pk=course_id)
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    student_assignment = get_object_or_404(Student_Assignment, pk=student_assignment_id)
    print("SUBMISSION",student_assignment.submission)
    return render(request, 'courses/student_assignment_detail.html', {'course': course, 'assignment': assignment, 'student_assignment': student_assignment})