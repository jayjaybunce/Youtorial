from django.shortcuts import render
from .utils import get_url_list

# Create your views here.
def homepage(request):
    context = {
        'urls': get_url_list(request),
        'title': 'Home',
    }
    return render(request, 'main_app/index.html', context)
def user_profile(request):
    context = {
        'urls': get_url_list(request),
        'title': 'User',
    }
    return render(request, 'main_app/user_profile.html' ,context)
def tutorials(request):
    context = {
        'urls': get_url_list(request),
        'title': 'Tutorials',
    }
    return render(request, 'main_app/tutorials.html' ,context)

def new_tutorial(request):
    context = {
        'urls': get_url_list(request),
        'title': 'Add Tutorial',
    }
    return render(request, 'main_app/new_tutorial.html' ,context)
def categories(request):
    context = {
        'urls': get_url_list(request),
        'title': 'Categories',
    }
    return render(request, 'main_app/categories.html' , context)

def about(request):
    context = {
        'urls': get_url_list(request),
        'title': 'About',
    }
    return render(request, 'main_app/about.html' ,context)









