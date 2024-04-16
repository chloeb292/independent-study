from django.urls import path
from .views import assignment_views, course_views, exam_views, quiz_views, user_views

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

    # path('course/<int:course_id>/assignment/new/', assignment_views.create_assignment, name='create_assignment'),
    # path('course/<int:course_id>/assignment/<int:assignment_id>/', assignment_views.assignment_detail, name='assignment_detail'),

    # path('course/<int:course_id>/quiz/new/', quiz_views.create_quiz, name='create_quiz'),
    # path('course/<int:course_id>/quiz/<int:quiz_id>/', quiz_views.quiz_detail, name='quiz_detail'),

    # path('course/<int:course_id>/exam/new/', exam_views.create_exam, name='create_exam'),
    # path('course/<int:course_id>/exam/<int:exam_id>/', exam_views.exam_detail, name='exam_detail'),

]