from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE
from datetime import datetime





class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Tutorial(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    rating = models.IntegerField(null=True)
    published = models.DateTimeField(auto_now_add=True, blank=True)
    language = models.CharField(max_length=200)
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_url = models.CharField(max_length=200,null=True,default='')
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }

    def __save__(self, *args, **kwargs):
        if self.published == None:
            self.published = timezone.now()

        return super(Tutorial, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user}, {self.title}'



class Status(models.Model):
    level_status = (
        ('S', 'Saved'),
        ('C', 'Completed'),
        ('G', 'Generated'),
    )
    stats = models.CharField(max_length= 100, choices = level_status, default=level_status[0][0])
    saved = models.DateTimeField("date saved", default=datetime.now())
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    tutorial = models.ForeignKey(Tutorial, on_delete=models.PROTECT)

    def __str__(self):
        return self.stats


class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user}, {self.content}'

class Photo(models.Model):
    url = models.CharField(max_length=200,default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Video(models.Model):
    url = models.CharField(max_length=200,default='')
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)






    





