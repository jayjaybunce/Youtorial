from django.contrib.auth.forms import UserCreationForm
from django.forms import fields
from django import forms
from django.contrib.auth.models import User
from .models import Tutorial
from tinymce.widgets import TinyMCE


class CreateUserForm(UserCreationForm):
    first_name = fields.CharField(max_length=200)
    last_name = fields.CharField(max_length=200)
    email_address = fields.CharField(max_length=200)
    class Meta:
        model = User
        fields = ('first_name','last_name','email_address')


class TutorialForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows':50,'class': 'form-control'}))
    
    class Meta:
        model = Tutorial
        fields = ['title','content','rating','language','category']



    


