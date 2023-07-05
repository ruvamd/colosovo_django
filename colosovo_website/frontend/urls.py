from django.urls import path
from . import views

urlpatterns = [
    path('', views.front_page, name='front_page'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]



