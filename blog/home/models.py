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
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    blog_content=models.TextField()
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class comments(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    comment=models.TextField()
    approved=models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username