from django.contrib import admin
from .models import Tutorial, Photo, Video, Comment, Category, User, Status
# Register your models here.
admin.site.register(Tutorial)
admin.site.register(Photo)
admin.site.register(Video)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Status)
