from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request, 'main_app/index.html')

def user_profile(request):
    return render(request, 'main_app/user_profile.html')