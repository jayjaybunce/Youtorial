from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .utils import get_url_list
import uuid
import boto3
from .models import Photo
from django.contrib.auth.models import User


S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = 'youtorial'


# Create your views here.
def homepage(request):
    context = {
        'urls': get_url_list(request),
        'title': 'Home',
    }
    return render(request, 'main_app/index.html', context)

def user_profile(request):
    try:
        photo = Photo.objects.get(user=request.user)
    except:
        photo = None
    context = {
        'urls': get_url_list(request),
        'title': 'User',
        'photo': photo,
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

def add_photo(request, user_id):
    photo_file = request.FILES.get('photo-file', None)
    try:
        photo = Photo.objects.get(user=request.user)
    except:
        photo = None
    if photo:
        photo.delete()
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, user_id=user_id)
            photo.save()
        except:
            print('An error occured uploading file e to S3')
    return redirect('user_profile')
    
    






