from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm  # If you don't have a custom ProfessorForm
from ..models import Professor
from django.contrib.auth.models import User
from django import forms


# Use a custom form if you have extra fields
class ProfessorSignUpForm(UserCreationForm):
    department = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        professor = Professor.objects.create(user=user)
        return user

def login_view(request):
    if request.user.is_authenticated:
        return redirect('course_list')  # Make sure this is the name used in your URL conf

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('course_list')  # Redirect to the main page after login
        else:
            error_message = 'Invalid username or password'
            return render(request, 'courses/login.html', {'error_message': error_message})

    return render(request, 'courses/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('course_list')

    if request.method == 'POST':
        form = ProfessorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('course_list')
        else:
            # Pass form errors back to the template
            return render(request, 'courses/register.html', {'form': form})
    else:
        form = ProfessorSignUpForm()

    return render(request, 'courses/register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Ensure 'login' is the correct name in your URL conf
