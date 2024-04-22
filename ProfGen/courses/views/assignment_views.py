from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from courses.models import Course, Assignment
from courses.forms import AssignmentForm
import google.generativeai as genai
import os, pathlib, textwrap
import markdown
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel('gemini-pro')


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
    # print("ANSWER KEY", assignment.answerkey)
    return render(request, 'courses/assignment_detail.html', {'course': course, 'assignment': assignment, 'answerkey': assignment.answerkey})

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
    if data['limit_to_selected'] and data['selected_materials']:
        user_input += "The assignment should be limited to the selected materials. Do not reference anything that is not found in the selected materials."
    
    user_input+="""

    Format and Elements for Assignments
    
    Title and Description:
    Begin with a clear title and a brief description of the assignments main objective or theme.
    
    Naming Rule:
    Each assignment includes a specific naming rule for the file(s) to be created.
    
    Programming Task Details:
    Detailed instructions are provided on what needs to be programmed. This includes:
    Specific functions to be implemented.
    Desired behavior and functionality of the program.
    Any specific methods, formulas, or approaches that should be used.
    Specific data structures or types that should be employed.
    
    Input/Output Requirements:
    Explicit instructions on how the program should handle input and output. This might involve:
    Reading from or writing to files.
    Handling user input via the command line.
    Formatting the output or results.
    
    Validation and Error Handling:
    Instructions on how to handle incorrect or unexpected inputs.
    Requirements for validating user inputs or data read from files.
    
    External Libraries or Modules:
    If applicable, instructions to use certain Python modules or external libraries, including how and where to use them in the program.
    
    Sample Output or Interaction:
    Providing examples of what the output should look like or how the user should interact with the program.
    For assignments involving user interaction, a walkthrough of a sample session may be provided.
    
    Points Allocation:
    Each assignment specifies how many points it is worth, often indicating a focus on assessment transparency.
    Patterns in Assignment Design
    Practical Application: Each assignment encourages applying theoretical knowledge to practical programming tasks, enhancing learning through doing.
    Incremental Complexity: Tasks typically build on basic concepts, gradually introducing complexity (e.g., starting with class creation, moving to file operations, then data visualization).
    Feedback Mechanisms: Sample outputs and interaction transcripts help students understand the expected program behavior and structure their code accordingly.
    Skill Reinforcement: Assignments often reinforce fundamental programming skills like class design, file I/O, data manipulation, and using libraries.
    
    Example Assignment Template:
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

    IMPORTANT: ASSIGNMENT MUST INCLUDE EACH OF THE ABOVE ELEMENTS TO ENSURE COMPLETENESS AND CLARITY. DO NOT DEVIATE FROM THE SPECIFIED FORMAT.

    """

    response = model.generate_content(user_input)

    response = response.text.strip()
    response = markdown.markdown(response)

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

    At the end of each question, you should have a comment that explains the code and how it meets the requirements of the rubric. This will help the student understand how the code solves the problem and why it is correct.
    
    """)
    
    
    response = model.generate_content(user_input)
    response = response.text.strip()
    assignment.answerkey = response
    assignment.save()

    # print(response)
    # print("ANSWER KEY", assignment.answerkey)
    return redirect('assignment_detail', course_id=course_id, assignment_id=assignment_id)
    
