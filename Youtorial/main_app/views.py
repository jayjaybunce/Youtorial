from django.shortcuts import render, redirect
from .utils import get_url_list
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm


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

def sign_up(request):
    email = request.POST['email']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    form = UserCreationForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        login(request, user)
        return redirect('homepage')
    else: 
        error_message_signup = 'Invalid signup - try again'
    context = {
        'error_message_signup': error_message_signup,
    }
    return redirect('homepage')
    
    






