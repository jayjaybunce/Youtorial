from django.urls import path
from . import views
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('user/', views.user_profile, name='user_profile'),
    path('tutorials/', views.tutorials, name='tutorials'),
    path('categories/', views.categories, name='categories'),
    path('tutorials/new/', views.new_tutorial, name='new_tutorial'),
    path('about/', views.about, name='about'),
]
