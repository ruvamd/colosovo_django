from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages


def front_page(request):
    return render(request, 'frontend/front_page.html')

def login_view(request):
    if request.method == 'POST':
        identifier = request.POST['identifier']
        password = request.POST['password']
        
        user = User.objects.filter(Q(username=identifier) | Q(email=identifier)).first()
        
        if user is not None and user.check_password(password):
            login(request, user)
            return redirect('front_page')  # Redirect to the front page after successful login
        else:
            # Handle invalid login credentials
            return render(request, 'frontend/login.html', {'error': 'Invalid username/email or password'})
    else:
        return render(request, 'frontend/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        email = request.POST['email']

        if password != password_confirm:
            messages.error(request, 'Password confirmation does not match.')
            return redirect('register')

        # Check if the email already exists in the database
        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered. Please choose a different email.')
            return redirect('register')

        # Proceed with user registration
        user = User.objects.create_user(username=username, password=password, email=email)
        login(request, user)
        return redirect('front_page')  # Redirect to the front page after successful registration
    else:
        return render(request, 'frontend/register.html')

def logout_view(request):
    logout(request)
    return redirect('front_page')

