from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class userdetail(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    img=models.ImageField(upload_to='profile_pics',blank=True)
    about=models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class blog_post(models.Model):
    user=models.ForeignKey(User,models.SET_NULL,null=True)
    title=models.CharField(max_length=256,unique=False)
    blog_content=models.TextField()
    updated=models.DateTimeField(auto_now=True)
    # published=models.DateTimeField()
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class comments(models.Model):
    user = models.ForeignKey(User,models.SET_NULL,null=True)
    comment=models.TextField()
    approved=models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username