from django.db.models import Q
from django.urls import reverse
from django.template.loader import render_to_string

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model,login,logout,authenticate
from django.contrib.auth.views import PasswordResetConfirmView,PasswordResetView
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.shortcuts import render, redirect
from django.core.mail import send_mail


def front_page(request):
    return render(request, 'frontend/front_page.html')

User = get_user_model()

def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.email_verified = True
        user.save()
        messages.success(request, 'Your email has been verified. You can now log in.')
    else:
        messages.error(request, 'Email verification failed. Please request a new verification email.')

    return redirect('login')  # Redirect to the login page

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
        # Include a "Forgot Password" link in your login template
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

        # Create an inactive user
        user = User.objects.create_user(username=username, password=password, email=email, is_active=False)

        # Generate a token for email verification
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token_link = reverse('activate', args=[uidb64, token])

        # Send an email to the user for email verification
        current_site = get_current_site(request)
        mail_subject = 'Activate your account'
        message = render_to_string('frontend/activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'token_link': token_link,
        })
        send_mail(mail_subject, message, 'your_email@example.com', [email])

        # Show a message to inform the user about email verification
        messages.success(request, 'Please check your email to activate your account.')

        return redirect('front_page')  # Redirect to the front page after successful registration
    else:
        return render(request, 'frontend/register.html')

def logout_view(request):
    logout(request)
    return redirect('front_page')

