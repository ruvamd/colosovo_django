from django.shortcuts import render

# Create your views here.
def front_page(request): 
    return render(request, 'frontend/front_page.html')

