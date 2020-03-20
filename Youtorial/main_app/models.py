from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=200)

class Tutorial(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    rating = models.IntegerField()
    published = models.DateTimeField()
    language = models.CharField(max_length=200)
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __save__(self, *args, **kwargs):
        if self.published == None:
            self.published = timezone.now()

        return super(Tutorial, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user}, {self.title}'

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user}, {self.content}'

class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)





