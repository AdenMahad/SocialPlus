from django.db import models
from django.urls import reverse 
from django.contrib.auth.models import User




# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length = 200)
    author = models.ForeignKey('auth.User',on_delete = models.CASCADE)
    body = models.TextField()
    created_date = models.DateTimeField( auto_now_add=True)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return self.title
    def get_absolute_url(self): # new
        return reverse('post_detail',args=[str(self.id)])
    
class Comment(models.Model):
    author = models.ForeignKey('auth.User',on_delete = models.CASCADE,)
    body = models.TextField()
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return self.body
    
    def get_absolute_url(self): # new
        return reverse('post_detail',args=[str(self.id)])
    
class LikeDislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.IntegerField()
