from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .utils import get_url_list
from .forms import TutorialForm
from .models import Photo, Category, Tutorial, Video, Status

import uuid
import boto3





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
    stats = Status.objects.all()
    try:
        photo = Photo.objects.get(user=request.user)
    except:
        photo = None
    context = {
        'urls': get_url_list(request),
        'title': 'User',
        'photo': photo,
        'tutorials': Tutorial.objects.filter(user=request.user),
        'stats': stats
    }
    return render(request, 'main_app/user_profile.html' ,context)

def tutorials(request):
    
    context = {
        'urls': get_url_list(request),
        'title': 'Tutorials',
    }
    return render(request, 'main_app/tutorials.html' ,context)

def new_tutorial(request):
    categories = Category.objects.all()
    url = ''
    if request.method == 'POST':
        video_file = request.FILES.get('video_url')
        if video_file:
            s3 = boto3.client('s3')
            key = uuid.uuid4().hex[:6] + video_file.name[video_file.name.rfind('.'):]
            try:
                s3.upload_fileobj(video_file, BUCKET, key)
                url = f"{S3_BASE_URL}{BUCKET}/{key}"
                
                # video = Video(url=url, tutorial_id=tutorial_id)
                # video.save()
            except:
                print('An error occured uploding file e to S3')
    # return redirect('tutorials')
        
        tut_form = TutorialForm(request.POST)
        tut = tut_form.save(commit=False)
        tut.user = request.user
        tut.video_url = url
        if tut_form.is_valid():
            tut_form.save()
        return redirect(f'/tutorials/{tut.id}')

    form = TutorialForm()
    context = {
        'urls': get_url_list(request),
        'title': 'Add Tutorial',
        'form': form,
        'categories': categories,
    }
    return render(request, 'main_app/new_tutorial.html' ,context)

def tutorial_detail(request, tutorial_id):
    tutorial = Tutorial.objects.get(id=tutorial_id)
    tutorial_form = TutorialForm()
    print(f"This is the tutorial: {tutorial}")
    return render(request, 'main_app/tutorial_detail.html', {'tutorial': tutorial, 'tutorial_form': tutorial_form})



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


def edit_tutorial(request, tutorial_id):
    tutorial = Tutorial.objects.get(id=tutorial_id)
    if request.method == 'POST':
        category = Category.objects.get(id=request.POST['category'])
        tutorial.title = request.POST['title']
        tutorial.content = request.POST['content']
        tutorial.language = request.POST['language']
        tutorial.category = category
        form = TutorialForm(request.POST)
        if form.is_valid():
            tutorial.save()
            return redirect('detail', tutorial_id=tutorial_id)
    form = TutorialForm(instance=tutorial)
    context = {
        'urls': get_url_list(request),
        'form': form,
        'tutorial': tutorial
    }
    return render(request, 'main_app/edit_tutorial.html', context)

def delete_tutorial(request, tutorial_id):
    Tutorial.objects.get(id=tutorial_id).delete()
    return redirect('/')
    
def saved_tutorials(request):
    stats = Status.objects.all()
    
    context = {'stats': stats}
    return render(request, 'main_app/saved_tutorials.html', context)













    
# def add_video(request, tutorial_id):
#     video_file = request.FILES.get('video-file', None)
#     if video_file:
#         s3 = boto3.client('s3')
#         key = uuid.uuid4().hex[:6] + video_file.name[video_file.name.rfind('.'):]
#         try:
#             s3.upload_fileobj(video_file, BUCKET, key)
#             url = f"{S3_BASE_URL}{BUCKET}/{key}"
#             video = Video(url=url, tutorial_id=tutorial_id)
#             video.save()
#         except:
#             print('An error occured uploding file e to S3')
#     return redirect('tutorials')
    





