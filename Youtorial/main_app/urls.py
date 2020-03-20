from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', LoginView.as_view(), name='homepage'),
    path('user/', views.user_profile, name='user_profile'),
    path('tutorials/', views.tutorials, name='tutorials'),
    path('categories/', views.categories, name='categories'),
    path('tutorials/new/', views.new_tutorial, name='new_tutorial'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login_user'),
    path('signup/', views.sign_up, name='signup')
]
