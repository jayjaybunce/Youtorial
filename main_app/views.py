from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .utils import get_url_list
from .forms import TutorialForm
from .models import Photo, Category, Tutorial, Video, Status, Comment
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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

@login_required
def user_profile(request):
    stats = Status.objects.filter(user=request.user)
    completed_stats = stats.filter(stats="C")
    saved_stats = stats.filter(stats="S")
    try:
        photo = Photo.objects.get(user=request.user)
    except:
        photo = None
    context = {
        'urls': get_url_list(request),
        'title': 'User',
        'photo': photo,
        'tutorials': Tutorial.objects.filter(user=request.user),
        'completed_stats': completed_stats,
        'saved_stats': saved_stats,
    }
    return render(request, 'main_app/user_profile.html' ,context)

def tutorials(request, category_name):
    category = Category.objects.get(name=category_name)
    tutorials = Tutorial.objects.filter(category=category.id)
    try:
        photo = Photo.objects.get(user_id=request.user.id)
    except Photo.DoesNotExist:
        photo = None
    all_stats = Status.objects.all()
    for tut in tutorials:
        tut.stats = []
        tut_stats = all_stats.filter(tutorial_id=tut.id)
        for stat in tut_stats:
            tut.stats.append(stat.user)
        for t in tutorials:
            try:
                p = Photo.objects.get(user_id=t.user.id)
                t.user_url = p.url
            except Photo.DoesNotExist:
                p = None
    context = {
        'urls': get_url_list(request),
        'title': 'title',
        'tutorials': tutorials,
        'category': category,
        'photo': photo,
    }
    return render(request, 'main_app/tutorials.html' ,context)

@login_required
def new_tutorial(request):
    categories = Category.objects.all()
    url = ''
    if request.method == 'POST':
        video_file = request.FILES.get('video')
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
        if request.POST['video_url']:
            v_url = request.POST['video_url']
            if 'youtube' in v_url:
                for index,letter in enumerate(v_url):
                    if letter == '=':
                        v_url = v_url[index+1:]
                        print(v_url)
                        break

            url = f'https://youtube.com/embed/{v_url}'
        print(url)
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
    comments = Comment.objects.filter(tutorial_id=tutorial_id)
    for comment in comments:
        try:
            comment.user_url = Photo.objects.get(user_id=comment.user).url
        except Photo.DoesNotExist:
            comment.user_url = None

    stats_list = []
    completed_list = []
    try:
        stats = Status.objects.filter(stats='S',tutorial_id=tutorial.id)
        for stat in stats:
            stats_list.append(stat.user)
        completed = Status.objects.filter(stats='C',tutorial_id=tutorial.id)
        for complete in completed:
            completed_list.append(complete.user)
    except Status.DoesNotExist:
        stats = None
    try:
        photo = Photo.objects.get(user_id=tutorial.user.id)
    except Photo.DoesNotExist:
        photo = None
    tutorial_form = TutorialForm()
    context = {
        'tutorial': tutorial, 
        'tutorial_form': tutorial_form,
        'photo': photo,
        'urls': get_url_list(request),
        'stats': stats_list,
        'completed': completed_list,
        'comments': comments,
        }
    print(f"This is the tutorial: {tutorial}")
    return render(request, 'main_app/tutorial_detail.html', context)



def categories(request):
    categories = Category.objects.all()
    context = {
        'urls': get_url_list(request),
        'title': 'Categories',
        'categories': categories,
        
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



@login_required
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

@login_required
def edit_tutorial(request, tutorial_id):
    
    tutorial = Tutorial.objects.get(id=tutorial_id)
    if request.method == 'POST':
        video_file = request.FILES.get('video')
        if video_file:
            s3 = boto3.client('s3')
            key = uuid.uuid4().hex[:6] + video_file.name[video_file.name.rfind('.'):]
            try:
                s3.upload_fileobj(video_file, BUCKET, key)
                url = f"{S3_BASE_URL}{BUCKET}/{key}"
                tutorial.video_url = url
                # video = Video(url=url, tutorial_id=tutorial_id)
                # video.save()
            except:
                print('An error occured uploding file e to S3')
    # return redirect('tutorials')
        if request.POST['video_url'] != '':
            v_url = request.POST['video_url']
            if 'youtube' in v_url:
                for index,letter in enumerate(v_url):
                    if letter == '=':
                        v_url = v_url[index+1:]
                        print(v_url)
                        break
                url = f'https://youtube.com/embed/{v_url}'
            else:
                url = request.POST['video_url']
            
                          

        if not request.FILES and not request.POST['video_url']:
            url = ''
        tutorial.video_url = url
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


@login_required
def delete_tutorial(request, tutorial_id):
    Tutorial.objects.get(id=tutorial_id).delete()
    return redirect('/user/')
    
def saved_tutorials(request):
    stats = Status.objects.all()
    
    context = {'stats': stats}
    return render(request, 'main_app/saved_tutorials.html', context)

@login_required
def save_tutorial(request, tutorial_id):
    prev_url = request.META.get('HTTP_REFERER')
    tutorial = Tutorial.objects.get(id=tutorial_id)
    status = Status()
    status.tutorial = tutorial
    status.user = request.user
    status.stats = "S"
    status.save()
    return redirect(prev_url)

@login_required
def unsave_tutorial(request,tutorial_id):
    print('do some things here')

@login_required
def complete_tutorial(request, tutorial_id):
    tutorial = Tutorial.objects.get(id=tutorial_id)
    status = Status()
    status.tutorial = tutorial
    status.user = request.user
    status.stats = "C"
    status.save()
    return redirect('user_profile')

@login_required
def add_comment(request, tutorial_id):
    prev_url = request.META.get('HTTP_REFERER')
    tutorial = Tutorial.objects.get(id=tutorial_id)
    comment = Comment(content=request.POST['content'],tutorial=tutorial,user=request.user)
    comment.save()
    return redirect(prev_url)


def add_category(request):
    prev_url = request.META.get('HTTP_REFERER')
    cat_name = request.POST['name']
    cat_photo_file = request.FILES['photo_url']
    url = ''
    print('url before upload',url)
    if cat_photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + cat_photo_file.name[cat_photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(cat_photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
        except:
            print('An error occured uploading file e to S3')
    category = Category(name=cat_name,photo_url=url)
    category.save()
    return redirect(prev_url)
    










    
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
    






