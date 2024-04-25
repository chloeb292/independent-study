from django.urls import path
from django.conf import settings
from .views import assignment_views, course_views, quiz_views, user_views
from django.conf.urls.static import static

urlpatterns = [
    path('login/', user_views.login_view, name='login'),
    path('register/', user_views.register_view, name='register'),
    path('logout/', user_views.logout_view, name='logout'),

    path('', course_views.course_list, name='course_list'),
    path('course/<int:course_id>/', course_views.course_detail, name='course_detail'),
    path('course/new/', course_views.create_course, name='create_course'),
    path('course/<int:course_id>/edit/', course_views.edit_course, name='edit_course'),

    path('course/<int:course_id>/upload/', course_views.upload_material, name='upload_material'),
    path('course/<int:course_id>/material/<int:material_id>/', course_views.material_detail, name='material_detail'),
    path('course/<int:course_id>/material/<int:material_id>/delete/', course_views.delete_material, name='delete_material'),

    path('course/<int:course_id>/assignment/new/', assignment_views.create_assignment, name='create_assignment'),
    path('course/<int:course_id>/assignment/<int:assignment_id>/', assignment_views.assignment_detail, name='assignment_detail'),
    # path('course/<int:course_id>/assignment/<int:assignment_id>/delete/', assignment_views.delete_assignment, name='delete_assignment'),
    path('course/<int:course_id>/assignment/<int:assignment_id>/generate_answer_key/', assignment_views.generate_answer_key, name='generate_answer_key'),

    path('course/<int:course_id>/quiz/new/', quiz_views.create_quiz, name='create_quiz'),
    path('course/<int:course_id>/quiz/<int:quiz_id>/', quiz_views.quiz_detail, name='quiz_detail'),
    # path('course/<int:course_id>/quiz/<int:quiz_id>/delete_quiz/', quiz_views.delete_quiz, name='delete_quiz'),
    path('course/<int:course_id>/quiz/<int:quiz_id>/generate_quiz_answer_key/', quiz_views.generate_quiz_answer_key, name='generate_quiz_answer_key'),

    path('course/<int:course_id>/assignment/<int:assignment_id>/grade_student_assignment/', assignment_views.grade_student_assignment, name='grade_student_assignment'),
    path('course/<int:course_id>/assignment/<int:assignment_id>/student_assignment_detail/<int:student_assignment_id>', assignment_views.student_assignment_detail, name='student_assignment_detail'),
    
    path('course/<int:course_id>/quiz/<int:quiz_id>/grade_student_quiz/', quiz_views.grade_student_quiz, name='grade_student_quiz'),
    path('course/<int:course_id>/quiz/<int:quiz_id>/student_quiz_detail/<int:student_quiz_id>', quiz_views.student_quiz_detail, name='student_quiz_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)