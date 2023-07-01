from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def front_page(request):
    return render(request, 'frontend/front_page.html')


