from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Post(models.Model):
    writer = models.ForeignKey(User,on_delete=models.CASCADE,)
    title = models.CharField(max_length=64)
    contents = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view_count = models.IntegerField(default=0)
    category = models.CharField(max_length=10,default='')
    likes = models.ManyToManyField(User,related_name='like_posts',blank=True)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField()
    post = models.ForeignKey(to='Post',on_delete=models.CASCADE)
    commenter = models.ForeignKey(to=User,on_delete=models.CASCADE)