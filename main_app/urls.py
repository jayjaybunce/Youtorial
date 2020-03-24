from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', LoginView.as_view(), name='homepage'),
    path('user/', views.user_profile, name='user_profile'),
    path('tutorials/categories/<str:category_name>/', views.tutorials, name='tutorials'),
    path('tutorials/<int:tutorial_id>/', views.tutorial_detail, name='detail'),
    path('categories/', views.categories, name='categories'),
    path('categories/<int:category_id>/delete/', views.categories_del, name='categories_del'),
    path('tutorials/new/', views.new_tutorial, name='new_tutorial'),
    path('tutorials/saved/', views.saved_tutorials, name='saved_tutorials'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login_user'),
    path('signup/', views.sign_up, name='signup'),
    path('user/<int:user_id>/add_photo', views.add_photo, name='add_photo'),
    path('tutorials/<int:tutorial_id>/edit/', views.edit_tutorial, name='edit_tutorial'),
    path('tutorials/<int:tutorial_id>/delete/', views.delete_tutorial, name='delete_tutorial'),
    path('tutorials/<int:tutorial_id>/save/', views.save_tutorial, name='save_tutorial')
    
    
    
]
