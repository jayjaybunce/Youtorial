from django.contrib.auth.forms import UserCreationForm
from django.forms import fields
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    first_name = fields.CharField(max_length=200)
    last_name = fields.CharField(max_length=200)
    email_address = fields.CharField(max_length=200)
    class Meta:
        model = User
        fields = ('first_name','last_name','email_address')
    


