from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
    # path('', views.front_page, name='front_page'),
    # path('users/', include('users.urls')),
    # path('users/', include('django.contrib.auth.urls')),
    # path('users/', include('django_registration.backends.activation.urls')),
    # path('users/', include('django.contrib.auth.urls')),
    # path('users/', include('django_registration.backends.one_step.urls')),
    # path('users/', include('django_registration.backends.activation.urls')),

    # Include default auth urls. 
    path('', include('django.contrib.auth.urls')),
    # Registration page. 
    path('register/', views.register,name='register'),
]
