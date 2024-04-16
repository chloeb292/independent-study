from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from ..models import Course, UploadedMaterial
from ..forms import CourseForm, UploadedMaterialForm

@login_required
def course_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required
def course_detail(request, course_id):
    if not request.user.is_authenticated:
        return redirect('login')
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'courses/course_detail.html', {'course': course})

@login_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)  # Do not immediately save to DB
            course.professor = request.user  # Set the professor to the current user
            course.save()  # Now save the course
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseForm()
    return render(request, 'courses/create_course.html', {'form': form})


@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            course = form.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/edit_course.html', {'form': form, 'course': course})

@login_required
def upload_material(request, course_id):
    course = get_object_or_404(Course, id=course_id, professor=request.user)
    if request.method == 'POST':
        form = UploadedMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.course = course
            material.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = UploadedMaterialForm()
    return render(request, 'courses/upload_material.html', {'form': form, 'course': course})

@login_required
def material_detail(request, course_id, material_id):
    material = get_object_or_404(UploadedMaterial, id=material_id, course_id=course_id)
    return render(request, 'courses/material_detail.html', {'material': material})
