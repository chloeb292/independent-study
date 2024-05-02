from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from courses.models import Course, Quiz, Student_Quiz
from courses.forms import QuizForm, StudentQuizAnswerForm
import google.generativeai as genai
import os, pathlib, textwrap
from dotenv import load_dotenv
import markdown
import pdfplumber
import pytesseract
from PIL import Image
from io import BytesIO


load_dotenv()

API_KEY = os.getenv('API_KEY')
genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel('gemini-pro')


# Create your views here.
@login_required
def create_quiz(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        form = QuizForm(request.POST, course=course)
        if form.is_valid():
            data = form.cleaned_data
            questions = generate_quiz_questions(data)

            quiz = form.save(commit=False)
            quiz.course = course
            quiz.questions = questions
            quiz.save()
            return redirect('course_detail', course_id=course_id)
    else:
        form = QuizForm(course=course)
    return render(request, 'courses/create_quiz.html', {'form': form, 'course': course})

def quiz_detail(request, course_id, quiz_id):
    course = get_object_or_404(Course, pk=course_id)
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    graded_quizes = Student_Quiz.objects.filter(quiz=quiz)
    return render(request, 'courses/quiz_detail.html', {'course': course, 'quiz': quiz, 'answerkey': quiz.answerkey, 'graded_quizes': graded_quizes})

def delete_quiz(course_id, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    quiz.delete()
    return redirect('course_detail', course_id=course_id)

def generate_quiz_questions(data):
    user_input = textwrap.dedent(f""" You are a professor creating a quiz for your course. You will generate a coding quiz that is {data['num_questions']} questions in length. This quiz is for college students so it should be challenging, and take at least 1-2 hours to complete. To complete the quiz the student must have a deep understanding of the topics that will be specified. You will incorperate the following requirements into this quiz:
    The title of the quiz is: {data['title']}.
    The description of the quiz is: {data['description']}.
    The goal of this quiz is: {data['goal_of_quiz']}.
    The programming language that the student must use is: {data['programming_language']}.
    The difficulty level of this quiz is: {data['difficulty_level']}.
    The number of questions in this quiz is: {data['num_questions']}.
    The total points for this quiz is: {data['total_points']}. Please distribute the points according to the difficulty of the questions.

    The quiz should have the following question types: {data['question_type']}.
    The quiz should have the following question formats: {data['question_style']}.                 
    """)

    if data['limit_to_selected'] and data['selected_materials']:
        user_input += "The quiz should be limited to the selected materials. Do not reference anything that is not found in the selected materials."
    
    user_input+= textwrap.dedent(f"""This quiz must be exclusively about the following topics: {data['topics_and_concepts']}

    IMPORTANT: DO NOT GENERATE AN ANSWER KEY FOR THIS QUIZ. When writing comments in the code, do not use '#', insted use '//' no matter the language. """)

    response = model.generate_content(user_input)

    response = response.text.strip()
    # response = markdown.markdown(response)

    return response


def generate_quiz_answer_key(request, course_id, quiz_id):  # Corrected view signature
    quiz = get_object_or_404(Quiz, pk=quiz_id)  # Correct object retrieval

    user_input = textwrap.dedent(f""" 
    You are a professor creating an answer key for a coding quiz given to your students. 
    Please create an answer key for the following quiz.
    Give full and complete answers.
                                 
    The format of the quiz answer key is as follows:
    Question 1: Answer
    Question 2: Answer
    Question 3: Answer
    etc.
                                 
    IMPORTANT: When writing comments in the code, do not use '#', simply write the comment or explanation.
    
    The quiz questions as follows:
    {quiz.questions}.
    """)  # Define user input for content generation

    response = model.generate_content(user_input)  # Generate answer key content
    quiz.answerkey = response.text.strip()  # Assign to quiz object
    quiz.save()  # Save updated quiz object

    return redirect('quiz_detail', course_id=course_id, quiz_id=quiz_id)

def extract_text_from_image(file):
    # Convert the file to an image object
    image = Image.open(file)
    text = pytesseract.image_to_string(image)
    
    return text

def extract_text_from_pdf(file):
    # extract text from a PDF file using pdfplumber and an in-memory file
    with pdfplumber.open(file) as pdf:
        text = " ".join(page.extract_text() for page in pdf.pages)
    return text


def grade_student_quiz(request, course_id, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    if request.method == 'POST':
        form = StudentQuizAnswerForm(request.POST, request.FILES)
    else:
        form = StudentQuizAnswerForm()

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
            else:
                form.add_error(None, "Please upload only PDF files.")
                return render(request, 'courses/grade_student_quiz.html', {'quiz': quiz, 'form': form})
            

        print("SUBMISSION TEXT", submission_text)   

        # Grade the quiz, compare submission to quiz.questions and quiz.answerkey (if quiz.answerkey exists, if not, generate one)
        if not quiz.answerkey:
            generate_quiz_answer_key(request, course_id, quiz_id)

        user_prompt = textwrap.dedent(f""" You are a professor grading a student's quiz. Please grade the following quiz according to the context of the quiz and the answer key provided.
        The student's submission is as follows:
            {submission_text}

        The quiz questions are as follows:
            {quiz.questions}

        The answer key is as follows:
            {quiz.answerkey}
        
        Please provide a grade for each question in the quiz. Explain why the student received the grade they did. If the student's answer is incorrect, provide feedback on how they can improve.
        """)

        response = model.generate_content(user_prompt)
        response = response.text.strip()
        print("RESPONSE", response)

        # Save the student's quiz and grade
        student_quiz = Student_Quiz(student_f_name=student_f_name, student_l_name=student_l_name, quiz=quiz, submission=submission_text, grade=response)
        student_quiz.save()

        return redirect('student_quiz_detail', course_id=course_id, quiz_id=quiz_id, student_quiz_id=student_quiz.id)
    return render(request, 'courses/grade_student_quiz.html', {'quiz': quiz, 'form': form})

def student_quiz_detail(request, course_id, quiz_id, student_quiz_id):
    course = get_object_or_404(Course, pk=course_id)
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    student_quiz = get_object_or_404(Student_Quiz, pk=student_quiz_id)
    return render(request, 'courses/student_quiz_detail.html', {'course': course, 'quiz': quiz, 'student_quiz': student_quiz})