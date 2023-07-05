from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.db.models import Q

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
        # Handle registration form submission
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        # Additional registration fields can be added based on your requirements

        # Create a new user and save it to the database
        user = User.objects.create_user(username=username, password=password, email=email)
        # You can also set additional user properties if needed, e.g., user.first_name, user.last_name, etc.

        return redirect('front_page')  # Redirect to the front page after successful registration
    else:
        # Render the registration form
        return render(request, 'frontend/register.html')

def logout_view(request):
    logout(request)
    return redirect('front_page')
